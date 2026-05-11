"use client";

import { useState, useEffect } from 'react';

interface FormattedDateProps {
  date?: string | Date;
  options?: Intl.DateTimeFormatOptions;
  locale?: string;
}

/**
 * A client-safe date formatter to avoid hydration mismatches.
 * Renders an empty span or a placeholder on the server and the actual date on the client.
 */
export default function FormattedDate({ 
  date, 
  options = { day: 'numeric', month: 'long', year: 'numeric' },
  locale = 'es-ES'
}: FormattedDateProps) {
  const [mounted, setMounted] = useState(false);
  const [dateObj, setDateObj] = useState<Date | null>(null);

  useEffect(() => {
    setMounted(true);
    setDateObj(date ? (typeof date === 'string' ? new Date(date) : date) : new Date());
  }, [date]);

  if (!mounted || !dateObj) {
    return <span className="inline-block w-20 h-4 bg-zinc-100 animate-pulse rounded" />;
  }

  return <span>{dateObj.toLocaleDateString(locale, options)}</span>;
}
