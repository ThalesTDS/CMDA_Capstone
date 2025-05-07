import React, {useEffect, useState} from 'react';
import {useMetrics} from '../../contexts/MetricsContext';
import {useTheme} from '../../contexts/ThemeContext';
import NativeDialogButton from '../common/NativeDialogButton';
import {Bubbles, SwimmingFish} from '../common/AquaticElements';

// Ship animation component factory - creates multiple ships with different properties
const createAnimatedShips = (count = 4) => {
    const {theme} = useTheme();

    // Create an array of ships with varying properties
    const ships = Array.from({length: count}, (_, index) => {
        // Calculate different delays, speeds, and positions
        const delay = index * 2; // 0s, 2s, 4s, 6s delay
        const speed = 35 + Math.random() * 15; // 35-50s base animation duration (faster)
        const position = 20 + (index * 15); // Different vertical positions
        const size = 120 + (index * 15); // Larger sizes

        return (
            <div
                key={index}
                className="absolute overflow-visible pointer-events-none z-20"
                style={{
                    top: `${position}%`,
                    transform: 'translateY(-50%)',
                    width: '100%',
                    height: '100px'
                }}
            >
                <div
                    className="ship-container absolute"
                    style={{
                        animation: `${theme === 'aquatic' ? 'ship-aquatic' : 'ship-neon'} ${speed}s linear ${delay}s infinite`,
                        left: '-200px',
                        position: 'absolute'
                    }}
                >
                    <svg
                        width={size}
                        height={size / 2}
                        viewBox="0 0 120 60"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        className={theme === 'aquatic' ? 'text-primary' : 'text-accent'}
                        style={{
                            filter: theme === 'neon' ? 'drop-shadow(0 0 8px rgba(0, 255, 255, 0.6))' : 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1))'
                        }}
                    >
                        <path
                            d="M10 30 L40 50 L100 50 L110 30 L100 10 L40 10 Z"
                            stroke="currentColor"
                            strokeWidth="3"
                            fill={theme === 'aquatic' ? 'rgba(0, 114, 181, 0.4)' : 'rgba(0, 255, 255, 0.4)'}
                        />
                        <path
                            d="M40 25 L40 35 L60 35 L60 25 Z"
                            stroke="currentColor"
                            strokeWidth="2"
                            fill={theme === 'aquatic' ? 'rgba(0, 114, 181, 0.6)' : 'rgba(0, 255, 255, 0.6)'}
                        />
                        <circle cx="80" cy="30" r="5" fill="currentColor"/>
                    </svg>
                </div>
            </div>
        );
    });

    return ships;
};

const AnimatedShips = () => {
    return <>{createAnimatedShips(4)}</>;
};

// Particle effect
const ParticleEffect = () => {
    const {theme} = useTheme();
    const particleCount = 50;

    const generateParticles = () => {
        const particles = [];

        for (let i = 0; i < particleCount; i++) {
            const size = Math.random() * 4 + 1;
            const left = Math.random() * 100;
            const top = Math.random() * 100;
            const duration = Math.random() * 20 + 10;
            const delay = Math.random() * 5;

            particles.push(
                <div
                    key={i}
                    className={`absolute rounded-full ${theme === 'aquatic' ? 'bg-primary/20' : 'bg-accent/30'}`}
                    style={{
                        width: `${size}px`,
                        height: `${size}px`,
                        left: `${left}%`,
                        top: `${top}%`,
                        animation: `float ${duration}s ease-in-out ${delay}s infinite`,
                    }}
                />
            );
        }

        return particles;
    };

    return (
        <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
            {generateParticles()}
        </div>
    );
};

// Wave animation
const WaveAnimation = () => {
    const {theme} = useTheme();

    return (
        <div className="absolute bottom-0 left-0 right-0 h-40 overflow-hidden z-0 pointer-events-none">
            <div className={`wave wave1 ${theme === 'aquatic' ? 'bg-primary/10' : 'bg-accent/10'}`}></div>
            <div className={`wave wave2 ${theme === 'aquatic' ? 'bg-primary/10' : 'bg-accent/10'}`}></div>
            <div className={`wave wave3 ${theme === 'aquatic' ? 'bg-primary/5' : 'bg-accent/5'}`}></div>
        </div>
    );
};

const WelcomePage = () => {
    const {analyzePath, isLoading, error} = useMetrics();
    const [analysisProgress, setAnalysisProgress] = useState(0);
    const [progressMessage, setProgressMessage] = useState('');
    const {theme} = useTheme();

    // Clear any errors and set up polling for analysis status
    useEffect(() => {
        let timer;

        // If analysis is in progress, poll for status updates
        if (isLoading) {
            timer = setInterval(async () => {
                try {
                    const response = await fetch('/api/status');
                    const status = await response.json();

                    setAnalysisProgress(status.progress || 0);
                    setProgressMessage(status.status_message || 'Processing...');

                    // If analysis is complete and successful, redirect to dashboard
                    if (!status.in_progress && status.result && status.result.code === 0) {
                        console.log('Analysis complete, redirecting to dashboard...');
                        // Force a small delay before redirect to ensure state is updated
                        setTimeout(() => {
                            window.location.href = '/dashboard';
                        }, 500);
                        clearInterval(timer); // Clear the interval to prevent multiple redirects
                    }
                } catch (err) {
                    console.error('Error checking analysis status:', err);
                }
            }, 1000);
        }

        return () => clearInterval(timer);
    }, [isLoading]);

    const handleFileSelect = (path) => {
        // Analyze the selected path
        analyzePath(path);
    };

    return (
        <div
            className={`flex flex-col items-center justify-center min-h-[calc(100vh-114px)] py-12 px-4 relative overflow-hidden ${theme === 'aquatic' ? 'bg-gradient-to-b from-background to-primary/5' : 'bg-gradient-to-b from-background to-neon-primary/20'}`}>
            <ParticleEffect/>
            <AnimatedShips/>
            <WaveAnimation/>
            {theme === 'aquatic' && (
                <>
                    <SwimmingFish count={5}/>
                    <Bubbles count={20}/>
                </>
            )}

            <div
                className="text-center max-w-xl mx-auto z-10 backdrop-blur-sm bg-card/80 p-8 rounded-xl shadow-lg animate-float border border-primary/20">
                <div className="mb-8">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        className={`w-24 h-24 mx-auto mb-4 text-primary animate-pulse-slow ${theme === 'neon' ? 'drop-shadow-[0_0_15px_rgba(138,43,226,0.7)]' : ''}`}
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                    </svg>
                    <h1 className={`text-3xl font-bold mb-2 ${theme === 'neon' ? 'text-accent drop-shadow-[0_0_8px_rgba(0,255,255,0.7)]' : ''}`}>
                        Welcome to DocuMetrics
                    </h1>
                    <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
                        Analyze and visualize the quality of your Python code documentation with NAVSEA's advanced
                        evaluation tool
                    </p>
                </div>

                <div className="mb-6 flex flex-col items-center">
                    <NativeDialogButton
                        onSelectPath={handleFileSelect}
                        isLoading={isLoading}
                        className="w-full"
                    />
                </div>

                {/* Only show error if there is one from the backend */}
                {error && error !== "No metrics data available. Please analyze a file or directory first." && (
                    <div
                        className="mt-6 p-3 bg-destructive/10 border border-destructive/30 text-destructive rounded-md">
                        {error.replace(/file or directory|file\/directory|file/gi, 'folder')}
                    </div>
                )}

                {isLoading && (
                    <div className="mt-6 p-4 border border-primary/30 rounded-md bg-primary/5">
                        <h3 className="font-medium mb-2">Analysis in Progress</h3>
                        <div className="h-2 bg-muted rounded-full mb-2 overflow-hidden">
                            <div
                                className="h-full bg-primary rounded-full transition-all duration-300"
                                style={{width: `${analysisProgress}%`}}
                            ></div>
                        </div>
                        <p className="text-sm text-muted-foreground">
                            {progressMessage || "Please wait while we analyze your code documentation..."}
                        </p>
                    </div>
                )}

                <div className="mt-12 text-sm text-muted-foreground">
                    <p>DocuMetrics analyzes Python code for documentation quality</p>
                    <p>The system evaluates comment density, completeness, accuracy, and conciseness</p>
                </div>
            </div>
        </div>
    );
};

export default WelcomePage;
