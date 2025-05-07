import React from 'react';

// Deterministic pseudo-random number generator based on index
function seededRandom(seed) {
    let x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
}

// Fish swimming animations for aquatic theme
export const SwimmingFish = ({count = 5}) => {
    // Alternate direction by index, and spread positions/delays
    const fish = Array.from({length: count * 2}, (_, index) => {
        const isLeft = index % 2 === 1; // Odd indices go left, even go right
        const baseSeed = index + 1;

        // Spread delays and positions more randomly and evenly
        const delay = seededRandom(baseSeed + 300) * 12; // 0-12s
        const size = 32 + Math.floor(seededRandom(baseSeed) * 16); // 32-48px
        const posY = 10 + seededRandom(baseSeed + 100) * 80; // 10-90%

        // Increase travel distance: start far off-screen and end far off-screen
        // Further increase so fish are not visible at start
        const startX = isLeft ? '160%' : '-60%';
        const endX = isLeft ? '-60%' : '160%';

        // Vary animation duration more significantly, stable per fish
        const duration = 14 + Math.floor(seededRandom(baseSeed + 200) * 26); // 14s to 40s

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
                    animation: `fish-swim-${index} ${duration}s linear infinite`,
                    animationDelay: `${delay}s`,
                    transform: !isLeft ? 'scaleX(-1)' : 'none', // Flip right-moving fish, so all face right
                    opacity: 0,
                    animationFillMode: 'forwards',
                }}
            >
                <style>
                    {`
            @keyframes fish-swim-${index} {
              0% { left: ${startX}; opacity: 0; }
              1% { opacity: 1; }
              100% { left: ${endX}; opacity: 1; }
            }
          `}
                </style>
                {/* Simple fish SVG */}
                <svg
                    width={size}
                    height={size * 0.6}
                    viewBox="0 0 48 28"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    className="text-primary/60"
                >
                    {/* Fish body */}
                    <ellipse cx="22" cy="14" rx="14" ry="10" fill="#0EA5E9" opacity="0.7"/>
                    {/* Fish tail */}
                    <polygon points="36,14 48,4 48,24" fill="#0EA5E9" opacity="0.5"/>
                    {/* Fish fin */}
                    <polygon points="18,10 24,6 22,14" fill="#38BDF8" opacity="0.7"/>
                    {/* Fish eye */}
                    <circle cx="16" cy="13" r="2" fill="#fff"/>
                    <circle cx="16" cy="13" r="1" fill="#0A4D68"/>
                </svg>
            </div>
        );
    });

    return <>{fish}</>;
};

// Bubbles rising effect for aquatic theme
export const Bubbles = ({count = 15}) => {
    // Create multiple bubbles with different sizes, delays, and positions
    const bubbles = Array.from({length: count}, (_, index) => {
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
export const Seaweed = ({count = 4}) => {
    const seaweed = Array.from({length: count}, (_, index) => {
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
                    style={{width: '100%', height: '100%'}}
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
                <SwimmingFish count={5}/>
                <Bubbles count={15}/>
                <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-primary/5 to-transparent"/>
            </div>
        </div>
    );
};
