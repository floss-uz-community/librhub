import { getRequestConfig } from "next-intl/server";
import { hasLocale } from "next-intl";
import { routing } from "./routing";
import * as fs from 'fs/promises';
import * as path from 'path';

async function loadTranslations(locale: string) {
  const localeDir = path.join(process.cwd(), 'locales', locale);
  try {
    const files = await fs.readdir(localeDir);
    const jsonFiles = files.filter(file => file.endsWith('.json'));
    
    const messages = {};
    for (const file of jsonFiles) {
      const content = (await import(`../../locales/${locale}/${file}`)).default;
      Object.assign(messages, content);
    }
    
    return messages;
  } catch (error) {
    console.error(`Error loading translations for locale ${locale}:`, error);
    return {};
  }
}

export default getRequestConfig(async ({ requestLocale }) => {
  const requested = await requestLocale;
  const locale = hasLocale(routing.locales, requested)
    ? requested
    : routing.defaultLocale;

  return {
    locale,
    messages: await loadTranslations(locale),
  };
});
