import { PRODUCT_INFO } from '@/shared/constants/data';
import { ModeToggle } from '@/shared/ui/theme-toggle';

const Footer = () => {
  return (
    <section>
      <div className="my-container">
        <div className="mt-8 flex flex-col justify-between gap-4 border-t pt-2 text-center text-sm font-medium text-muted-foreground lg:flex-row lg:items-center lg:text-left">
          <p>
            © {new Date().getFullYear()} {PRODUCT_INFO.creator}. All rights
            reserved.
          </p>
          <div className='flex items-center gap-4'>
            <ul className="flex justify-center gap-4 lg:justify-start">
              <li className="hover:text-primary">
                <a href={PRODUCT_INFO.terms_of_use}>Terms and Conditions</a>
              </li>
            </ul>
            <ModeToggle />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Footer;
