import React, {useEffect, useState} from 'react';
import Header from './Header';
import {useTheme} from '../../contexts/ThemeContext';
import {AquaticBackground} from '../common/AquaticElements';

const MainLayout = ({children}) => {
    const {theme} = useTheme();
    const [scrollY, setScrollY] = useState(0);

    // Handle scroll for parallax effects
    useEffect(() => {
        const handleScroll = () => {
            setScrollY(window.scrollY);
        };

        window.addEventListener('scroll', handleScroll, {passive: true});
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <div
            className={`min-h-screen flex flex-col bg-background text-foreground transition-theme overflow-hidden ${theme === 'neon' ? 'neon-theme-wrapper' : 'aquatic-theme-wrapper'}`}>
            {/* Background elements */}
            {theme === 'neon' && (
                <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
                    <div
                        className="absolute top-0 left-0 w-full h-screen bg-gradient-to-b from-[#120c29] via-[#0D0C22] to-[#1A1A3A] opacity-40"
                        style={{transform: `translateY(${scrollY * 0.1}px)`}}
                    />
                    <div
                        className="absolute h-96 w-96 rounded-full bg-purple-600/10 blur-3xl top-20 -right-20"
                        style={{transform: `translateY(${scrollY * 0.2}px)`}}
                    />
                    <div
                        className="absolute h-64 w-64 rounded-full bg-cyan-500/10 blur-3xl top-1/2 left-10"
                        style={{transform: `translateY(${scrollY * -0.15}px)`}}
                    />
                </div>
            )}

            {theme === 'aquatic' && (
                <>
                    <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
                        <div
                            className="absolute top-0 left-0 w-full h-screen bg-gradient-to-b from-[#F0F8FF] via-[#F0F8FF] to-[#E0F4FF] opacity-60"
                            style={{transform: `translateY(${scrollY * 0.1}px)`}}
                        />
                        <div
                            className="absolute h-96 w-96 rounded-full bg-blue-300/10 blur-3xl bottom-20 -left-20"
                            style={{transform: `translateY(${scrollY * 0.2}px)`}}
                        />
                        <div
                            className="absolute h-64 w-64 rounded-full bg-cyan-300/10 blur-3xl top-1/3 -right-10"
                            style={{transform: `translateY(${scrollY * -0.15}px)`}}
                        />
                    </div>
                    <AquaticBackground/>
                </>
            )}

            <Header/>

            <main className="flex-grow relative z-10">
                {children}
            </main>

            <footer
                className={`${theme === 'neon' ? 'bg-neon-surface/50 shadow-[0_-5px_15px_rgba(0,0,0,0.1)]' : 'bg-card shadow-sm'} py-3 mt-8 relative z-10`}>
                <div className="wrapper">
                    <div className="flex justify-between items-center">
                        <div className="text-sm text-muted-foreground">
                            DocuMetrics - NAVSEA Documentation Evaluation Tool
                        </div>
                        <div className="text-xs text-muted-foreground">
                            v1.1.0
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default MainLayout;