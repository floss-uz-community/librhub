import { loadYamlConfig, getConfigValue } from "./yaml";

export interface AppConfig {
  app: {
    name: string;
    version: string;
  };
  server: {
    port: number;
    host: string;
  };
  features: {
    darkMode: boolean;
    analytics: boolean;
  };
  api: {
    baseUrl: string;
    timeout: number;
    endpoints: Array<{
      name: string;
      path: string;
      methods: string[];
    }>;
  };
}

export const config = loadYamlConfig<AppConfig>("app");

export const getAppName = () =>
  getConfigValue<string>(config, "app.name", "Default App Name");
export const getApiBaseUrl = () =>
  getConfigValue<string>(config, "api.baseUrl", "");
export const isDarkModeEnabled = () =>
  getConfigValue<boolean>(config, "features.darkMode", false);
export const getApiEndpoint = (name: string) => {
  const endpoints = getConfigValue<
    Array<{ name: string; path: string; methods: string[] }>
  >(config, "api.endpoints", []);
  return endpoints?.find((endpoint) => endpoint.name === name);
};

export default config;
