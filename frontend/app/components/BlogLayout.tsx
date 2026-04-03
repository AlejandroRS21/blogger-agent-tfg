/**
 * BlogLayout Component (Legacy Internal Wrapper)
 * 
 * Note: RootLayout in app/layout.tsx provides the global wrapper.
 * This component can be used for secondary page layouts if needed.
 */

import { ReactNode } from 'react';

interface BlogLayoutProps {
  children: ReactNode;
  className?: string;
}

export default function BlogLayout({ children, className = '' }: BlogLayoutProps) {
  return (
    <div className={`flex-grow ${className}`}>
      {children}
    </div>
  );
}
