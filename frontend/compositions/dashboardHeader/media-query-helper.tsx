import * as React from 'react';

export function useMediaQuery(width: number): boolean {
  const [targetReached, setTargetReached] = React.useState(false);

  const updateTarget = React.useCallback((e) => {
    setTargetReached(e.matches);
  }, []);

  React.useEffect(() => {
    const media = window.matchMedia(`(max-width: ${width}px)`);
    media.addEventListener('change', e => updateTarget(e));

    if (media.matches) {
      setTargetReached(true);
    }

    return () => media.removeEventListener('change', e => updateTarget(e));
  }, []);

  return targetReached;
};