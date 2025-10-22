import React, { createContext, useContext, useState } from 'react';

// Create context for sharing state across tabs
const AppContext = createContext();

// Custom hook to use the context
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider');
  }
  return context;
};

// Provider component
export const AppProvider = ({ children }) => {
  // Sales Coach Configuration State
  const [salesCoachConfig, setSalesCoachConfig] = useState({
    globalParams: {
      num_users: 100,
      assessments_per_user_per_month: 40
    },
    agentConfigs: {}, // Will be populated by SalesCoach component
    lastUpdated: null
  });

  // Function to update Sales Coach config from SalesCoach tab
  const updateSalesCoachConfig = (globalParams, agentConfigs) => {
    setSalesCoachConfig({
      globalParams,
      agentConfigs,
      lastUpdated: new Date().toISOString()
    });
  };

  // Function to convert Sales Coach config to Cost Calculator format
  const getSalesCoachCostParams = () => {
    const { globalParams, agentConfigs } = salesCoachConfig;

    // Calculate total queries (assessments in this case)
    const queries_per_user_per_month = globalParams.assessments_per_user_per_month || 40;

    // Calculate average tokens and LLM weights based on agent configurations
    let totalInputTokens = 0;
    let totalOutputTokens = 0;
    let totalWeight = 0;
    const llmWeights = {}; // Track weight per LLM model

    Object.values(agentConfigs).forEach(config => {
      if (config.usage_probability > 0) {
        const agentTokens = config.avg_tokens_per_request || 5000;
        const requests = config.requests_per_4cs_calculation || 1;
        const probability = config.usage_probability / 100;

        // Weight = probability × requests (how much this agent is used)
        const weight = probability * requests;

        totalInputTokens += agentTokens * 0.7 * weight;
        totalOutputTokens += agentTokens * 0.3 * weight;
        totalWeight += weight;

        // Track LLM usage weight
        if (config.llm) {
          llmWeights[config.llm] = (llmWeights[config.llm] || 0) + weight;
        }
      }
    });

    // Calculate weighted averages
    const avg_input_tokens = totalWeight > 0 ? Math.round(totalInputTokens / totalWeight) : 10000;
    const avg_output_tokens = totalWeight > 0 ? Math.round(totalOutputTokens / totalWeight) : 1000;

    // Calculate llm_mix as percentage distribution
    const llm_mix = {};
    if (totalWeight > 0) {
      Object.keys(llmWeights).forEach(llm => {
        llm_mix[llm] = (llmWeights[llm] / totalWeight) * 100;
      });
    } else {
      // Default mix if no configs
      llm_mix['gpt-4o'] = 60.0;
      llm_mix['claude-3.5-sonnet'] = 30.0;
      llm_mix['llama-3.1-70b'] = 10.0;
    }

    return {
      // NOTE: agent_type is NOT included here - it will be preserved by the merge in CostCalculator
      num_users: globalParams.num_users || 100,
      queries_per_user_per_month,
      avg_input_tokens,
      avg_output_tokens,
      llm_mix,
      infrastructure_scale: 1.0,
      cache_hit_rate: 0.70,
      use_prompt_caching: true,
      use_reserved_instances: true
    };
  };

  const value = {
    salesCoachConfig,
    updateSalesCoachConfig,
    getSalesCoachCostParams
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
