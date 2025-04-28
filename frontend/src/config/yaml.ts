import fs from "fs";
import path from "path";
import yaml from "js-yaml";

/**
 * Load and parse a YAML configuration file
 * @param fileName - Name of the YAML file to load (without extension)
 * @returns Parsed YAML content as object
 */
export function loadYamlConfig<T = any>(fileName: string): T {
  try {
    const configPath = path.join(
      process.cwd(),
      "src",
      "config",
      `${fileName}.yaml`
    );
    const fileContents = fs.readFileSync(configPath, "utf8");
    const data = yaml.load(fileContents) as T;
    return data;
  } catch (error) {
    console.error(`Error loading YAML config ${fileName}.yaml:`, error);
    throw error;
  }
}

/**
 * Get a nested value from a configuration object using dot notation
 * @param config - Configuration object
 * @param path - Path to the value using dot notation (e.g., 'app.name')
 * @param defaultValue - Default value to return if path not found
 * @returns The value at the specified path or the default value
 */
export function getConfigValue<T>(
  config: any,
  path: string,
  defaultValue?: T
): T | undefined {
  const keys = path.split(".");
  let current = config;

  for (const key of keys) {
    if (
      current === undefined ||
      current === null ||
      typeof current !== "object"
    ) {
      return defaultValue;
    }
    current = current[key];
  }

  return current !== undefined ? (current as T) : defaultValue;
}
