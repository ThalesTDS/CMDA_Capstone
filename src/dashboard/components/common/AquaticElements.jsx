import React from 'react';

// Fish swimming animations for aquatic theme
export const SwimmingFish = ({ count = 5 }) => {
  // Create multiple fish with different delays and positions
  const fish = Array.from({ length: count * 2 }, (_, index) => {
    const isLeft = index >= count; // Determine if fish is on the left side
    const delay = (index % count) * 3; // Spread out fish animations
    const size = 24 + ((index % count) % 3) * 8; // Vary sizes
    const posY = 30 + ((index % count) * 12); // Different vertical positions

    // Increase travel distance: start far off-screen and end far off-screen
    // Animate from -30% to 130% (or reverse for left-facing)
    const startX = isLeft ? '-30%' : '-30%';
    const endX = isLeft ? '130%' : '130%';

    // Vary animation duration more significantly
    const duration = 12 + Math.random() * 28; // 12s to 40s

    return (
      <div
        key={index}
        className={`absolute z-10`}
        style={{
          top: `${posY}%`,
          left: 0,
          width: `${size}px`,
          height: `${size * 0.6}px`,
          pointerEvents: 'none',
          // Custom swim animation per fish
          animation: `fish-swim-${index} ${duration}s linear infinite`,
          animationDelay: `${delay}s`,
          transform: isLeft ? 'scaleX(-1)' : 'none',
        }}
      >
        <style>
          {`
            @keyframes fish-swim-${index} {
              0% { left: ${isLeft ? endX : startX}; }
              100% { left: ${isLeft ? startX : endX}; }
            }
          `}
        </style>
        <svg
          width={size}
          height={size * 0.6}
          viewBox="0 0 24 16"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="text-primary/50"
        >
          <path
            d="M18 8c0 2.5-4 6-10 6C4 14 2 12.5 2 10.5S4 8 8 8c6 0 10 -2.5 10-6S14 0 8 0C4 0 2 1.5 2 3.5M2 3.5V10.5M6 5l-2 1.5M6 11l-2-1.5"
            stroke="currentColor"
            strokeWidth="1"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <circle cx="5" cy="7" r="1" fill="currentColor" />
        </svg>
      </div>
    );
  });

  return <>{fish}</>;
};

// Bubbles rising effect for aquatic theme
export const Bubbles = ({ count = 15 }) => {
  // Create multiple bubbles with different sizes, delays, and positions
  const bubbles = Array.from({ length: count }, (_, index) => {
    const delay = index * 0.5; // Spread out bubble animations
    const size = 4 + Math.random() * 12; // Random sizes
    const posX = Math.random() * 100; // Random horizontal positions
    
    return (
      <div 
        key={index}
        className="absolute rounded-full bg-primary/20 animate-bubbles-rise"
        style={{ 
          width: `${size}px`,
          height: `${size}px`,
          left: `${posX}%`,
          bottom: '0',
          animationDelay: `${delay}s`,
          animationDuration: `${10 + Math.random() * 15}s`
        }}
      />
    );
  });
  
  return <>{bubbles}</>;
};

// Seaweed animation for aquatic theme
export const Seaweed = ({ count = 4 }) => {
  const seaweed = Array.from({ length: count }, (_, index) => {
    const posX = 10 + (index * 25); // Space out horizontally
    const height = 80 + Math.random() * 80; // Vary heights
    const width = 20 + Math.random() * 20; // Vary widths
    const animationDuration = 3 + Math.random() * 4; // Vary animation speeds
    
    return (
      <div 
        key={index}
        className="absolute bottom-0 origin-bottom"
        style={{ 
          left: `${posX}%`,
          height: `${height}px`,
          width: `${width}px`,
          animation: `sway ${animationDuration}s ease-in-out infinite alternate`
        }}
      >
        <svg 
          viewBox="0 0 50 200" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
          style={{ width: '100%', height: '100%' }}
        >
          <path 
            d="M25 0 Q40 50 10 100 Q40 150 25 200" 
            stroke="#0E7490" 
            strokeWidth="8" 
            strokeLinecap="round" 
            fill="none" 
            opacity="0.3"
          />
        </svg>
      </div>
    );
  });
  
  return <>{seaweed}</>;
};

// Combined aquatic background for the theme
export const AquaticBackground = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      <div className="relative w-full h-full">
      <SwimmingFish count={5} />
      <Bubbles count={15} />
      <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-primary/5 to-transparent" />
    </div>
    </div>
  );
};

// Add this style to your global.css
// @keyframes sway {
//   0% { transform: rotate(-5deg); }
//   100% { transform: rotate(5deg); }
// }
