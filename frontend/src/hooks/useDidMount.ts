import { useEffect, useState } from "react";

/**
 * Hook that returns true when the component has mounted.
 * Useful for avoiding hydration mismatches when dealing with browser-only APIs.
 *
 * @returns {boolean} Whether the component has mounted
 *
 * @example
 * const isMounted = useDidMount();
 * if (!isMounted) return null; // Skip rendering until client-side
 */
export function useDidMount(): boolean {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  return isMounted;
}
