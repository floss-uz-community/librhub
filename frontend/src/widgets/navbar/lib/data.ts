import { LanguageRoutes } from '@/shared/config/i18n/types';
import { MenuItem } from './model';

const menu: MenuItem[] = [
  // { title: 'Home', url: '#' },
  // {
  //   title: 'Blog',
  //   url: '#',
  // },
  // {
  //   title: 'News',
  //   url: '#',
  // },
];

const languages: { name: string; key: LanguageRoutes }[] = [
  {
    name: "O'zbekcha",
    key: LanguageRoutes.UZ,
  },
  {
    name: 'Ўзбекча',
    key: LanguageRoutes.KI,
  },
  {
    name: 'Русский',
    key: LanguageRoutes.RU,
  },
];

export { languages, menu };

