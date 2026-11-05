import { Link } from 'react-router-dom';

interface BrandLogoProps {
  to?: string;
  size?: 'sm' | 'md' | 'lg';
  showTagline?: boolean;
  className?: string;
  variant?: 'full' | 'compact';
  onDark?: boolean;
}

export default function BrandLogo({
  to = '/',
  size = 'md',
  showTagline = false,
  className = '',
  variant = 'compact',
  onDark = false,
}: BrandLogoProps) {
  const sizeMap = {
    sm: { img: 'h-7 w-7 sm:h-8 sm:w-8', text: 'text-sm sm:text-base', sub: 'text-[9px]' },
    md: { img: 'h-8 w-8 sm:h-9 sm:w-9', text: 'text-[15px] sm:text-lg', sub: 'text-[10px]' },
    lg: { img: 'h-10 w-10 sm:h-12 sm:w-12', text: 'text-xl sm:text-2xl', sub: 'text-xs' },
  };

  const currentSize = sizeMap[size];

  const content = (
    <div className={`inline-flex items-center gap-2 sm:gap-2.5 font-bold tracking-tight select-none ${className}`}>
      <img
        src="/logo.png"
        alt="HighonLearning Logo"
        className={`${currentSize.img} shrink-0 rounded-lg object-contain bg-white/5`}
        loading="eager"
      />
      {variant === 'compact' ? (
        <div className="flex flex-col leading-none whitespace-nowrap min-w-0">
          <span className={`${currentSize.text} font-black tracking-tight font-sans`}>
            <span className={onDark ? 'text-white' : 'text-navy-900'}>High</span>
            <span className="text-sky-500">on</span>
            <span className="text-amber-500">Learning</span>
          </span>
          {showTagline && (
            <span className={`mt-0.5 tracking-wider font-semibold uppercase ${onDark ? 'text-sky-200' : 'text-navy-400'} ${currentSize.sub}`}>
              Learn • Practice • Achieve
            </span>
          )}
        </div>
      ) : null}
    </div>
  );

  if (to) {
    return (
      <Link to={to} className="inline-flex items-center hover:opacity-95 transition-opacity">
        {content}
      </Link>
    );
  }

  return content;
}
