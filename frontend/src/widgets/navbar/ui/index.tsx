import { Accordion } from '@/shared/ui/accordion';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import {
  NavigationMenu,
  NavigationMenuList,
} from '@/shared/ui/navigation-menu';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/shared/ui/sheet';
import { Menu, Search } from 'lucide-react';
import { menu } from '../lib/data';
import { PRODUCT_INFO } from '@/shared/constants/data';
import RenderMenuItem from './RenderItem';
import RenderMobileMenuItem from './RenderMobileMenuItem';
import { ChangeLang } from './ChangeLang';
import Link from 'next/link';

const Navbar = () => {
  const auth = {
    login: { title: 'Login', url: '#' },
    signup: { title: 'Sign up', url: '#' },
  };

  return (
    <section className="py-4">
      <div className="my-container">
        {/* Desktop Menu */}
        <nav className="hidden justify-between lg:flex">
          <div className="flex items-center gap-6">
            {/* Logo */}
            <Link href={'/'} className="flex items-center gap-2">
              <span className="text-lg font-semibold tracking-tighter">
                {PRODUCT_INFO.name}
              </span>
            </Link>
            <div className="flex items-center">
              <NavigationMenu>
                <NavigationMenuList>
                  {menu.map((item) => RenderMenuItem(item))}
                </NavigationMenuList>
              </NavigationMenu>
            </div>
          </div>
          {/* Search Input */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
            <Input
              type="search"
              placeholder="Search posts..."
              className="pl-10 w-98"
            />
          </div>
          <div className="flex items-center gap-4">
            <div className="flex gap-2">
              <ChangeLang />
              <Button asChild variant="outline">
                <Link href={auth.login.url}>{auth.login.title}</Link>
              </Button>
              <Button asChild>
                <Link href={auth.signup.url}>{auth.signup.title}</Link>
              </Button>
            </div>
          </div>
        </nav>

        {/* Mobile Menu */}
        <div className="block lg:hidden">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link href={'/'} className="flex items-center gap-2">
              <img
                src={PRODUCT_INFO.logo}
                className="max-h-8"
                alt={PRODUCT_INFO.name}
              />
            </Link>
            <Sheet>
              <div className="space-x-2">
                <ChangeLang />
                <SheetTrigger asChild>
                  <Button variant="outline" size="icon">
                    <Menu className="size-4" />
                  </Button>
                </SheetTrigger>
              </div>
              <SheetContent className="overflow-y-auto">
                <SheetHeader>
                  <SheetTitle>
                    <Link href={'/'} className="flex items-center gap-2">
                      <img
                        src={PRODUCT_INFO.logo}
                        className="max-h-8"
                        alt={PRODUCT_INFO.name}
                      />
                    </Link>
                  </SheetTitle>
                </SheetHeader>
                <div className="flex flex-col gap-6 p-4">
                  {/* Mobile Search */}
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                    <Input
                      type="search"
                      placeholder="Search posts..."
                      className="pl-10 w-full"
                    />
                  </div>

                  <Accordion
                    type="single"
                    collapsible
                    className="flex w-full flex-col gap-4"
                  >
                    {menu.map((item) => RenderMobileMenuItem(item))}
                  </Accordion>

                  <div className="flex flex-col gap-3">
                    <Button asChild variant="outline">
                      <Link href={auth.login.url}>{auth.login.title}</Link>
                    </Button>
                    <Button asChild>
                      <Link href={auth.signup.url}>{auth.signup.title}</Link>
                    </Button>
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Navbar;
