import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, NavLink } from 'react-router-dom';
import { Shield, Brain, BarChart3, Lock, Zap, LogOut, CheckCircle2, ShieldAlert } from 'lucide-react';
import { motion } from 'framer-motion';

import ScamSimulation from './components/ScamSimulation';
import ScamChecker from './components/ScamChecker';
import UserDashboard from './components/UserDashboard';
import InstitutionalDashboard from './components/InstitutionalDashboard';

import './App.css';
import './Simulation.css';

const LandingPage = () => (
    <div className="landing">
        <section className="hero">
            <div className="container">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1 }}
                    className="hero-content"
                >
                    <div className="badge">AI-Powered Cybersecurity Simulation</div>
                    <h1 className="hero-title">
                        Build Your <span className="gradient-text">Digital Immunity</span> <br />
                        Before the Attack Happens.
                    </h1>
                    <p className="hero-subtitle">
                        Most cybersecurity training is passive. CyberGuard AI tests you with real-world simulations,
                        detects your psychological vulnerabilities, and builds a custom risk profile to keep you safe.
                    </p>
                    <div className="hero-actions">
                        <Link to="/simulator-demo" className="btn-primary">Try Simulator Demo</Link>
                        <Link to="/scam-checker" className="btn-outline">Analyze a Message</Link>
                    </div>
                </motion.div>

                <div className="hero-visual">
                    <div className="hero-card-stack">
                        <motion.div
                            className="glass-card hero-card main-card"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.5, duration: 1 }}
                        >
                            <div className="card-header">
                                <Brain className="card-icon" />
                                <span>AI Risk Assessment</span>
                            </div>
                            <div className="risk-meter">
                                <div className="meter-value" style={{ width: '68%' }}></div>
                            </div>
                            <div className="card-stat">
                                <h3>Vulnerability Score: 68</h3>
                                <p>Status: <span className="text-warning">At Risk</span></p>
                            </div>
                            <div className="weakness">
                                <span>Weakness: </span>
                                <span className="badge-small">Authority Bias</span>
                            </div>
                        </motion.div>
                        <div className="glass-card decoration-card c1"></div>
                        <div className="glass-card decoration-card c2"></div>
                    </div>
                </div>
            </div>
        </section>

        <section className="features">
            <div className="container">
                <h2 className="section-title text-center">Beyond Education: <span className="gradient-text">Behavioral Testing</span></h2>
                <div className="features-grid">
                    {[
                        { icon: <Zap />, title: "Real-World Simulations", desc: "We send safe, controlled phishing messages to test your reactions in real-time." },
                        { icon: <Brain />, title: "Psychological Profiling", desc: "Identify if you fall for greed, fear, urgency, or authority-based triggers." },
                        { icon: <BarChart3 />, title: "Dynamic Risk Score", desc: "Get a live digital immunity score that improves as you learn and resist scams." },
                        { icon: <Lock />, title: "Adaptive Training", desc: "The platform gets harder as you improve, ensuring you're always one step ahead." }
                    ].map((f, i) => (
                        <motion.div
                            key={i}
                            className="glass-card feature-card"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: i * 0.1 }}
                        >
                            <div className="feature-icon">{f.icon}</div>
                            <h3>{f.title}</h3>
                            <p className="text-muted">{f.desc}</p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    </div>
);

function App() {
    const [userRole, setUserRole] = useState(null); // 'user', 'admin', null

    return (
        <Router>
            <div className="app-wrapper">
                <nav className="navbar glass-card">
                    <div className="container nav-container">
                        <Link to="/" className="logo">
                            <Shield className="logo-icon" />
                            <span>CyberGuard <span className="gradient-text">AI</span></span>
                        </Link>

                        <div className="nav-links">
                            <NavLink to="/" end className={({ isActive }) => isActive ? "active" : ""}>Home</NavLink>
                            <NavLink to="/simulator-demo" className={({ isActive }) => isActive ? "active" : ""}>Simulation</NavLink>
                            <NavLink to="/scam-checker" className={({ isActive }) => isActive ? "active" : ""}>Scam Checker</NavLink>

                            {userRole ? (
                                <>
                                    {userRole === 'admin' ? (
                                        <NavLink to="/admin" className={({ isActive }) => isActive ? "active" : ""}>Institution</NavLink>
                                    ) : (
                                        <NavLink to="/dashboard" className={({ isActive }) => isActive ? "active" : ""}>Profile</NavLink>
                                    )}
                                    <button className="btn-logout" onClick={() => setUserRole(null)} title="Log Out"><LogOut size={18} /></button>
                                </>
                            ) : (
                                <div style={{ display: 'flex', gap: '1rem' }}>
                                    <button className="btn-outline" onClick={() => setUserRole('user')} style={{ padding: '0.4rem 1rem' }}>User Login</button>
                                    <button className="btn-primary" onClick={() => setUserRole('admin')} style={{ padding: '0.4rem 1rem' }}>Admin Portal</button>
                                </div>
                            )}
                        </div>
                    </div>
                </nav>

                <main>
                    <Routes>
                        <Route path="/" element={<LandingPage />} />

                        <Route path="/simulator-demo" element={
                            <div style={{ paddingTop: '6rem' }}>
                                <ScamSimulation onComplete={() => window.location.href = '/dashboard'} />
                            </div>
                        } />

                        <Route path="/dashboard" element={
                            userRole === 'user' ? (
                                <div className="dashboard-view" style={{ paddingTop: '6rem' }}>
                                    <div className="sim-cta text-center" style={{ padding: '2rem' }}>
                                        <Link to="/simulator-demo" className="btn-primary">Launch New Simulation Test</Link>
                                    </div>
                                    <UserDashboard />
                                </div>
                            ) : (
                                <div className="container" style={{ paddingTop: '10rem', textAlign: 'center' }}>
                                    <h2>Please login as User to view profile</h2>
                                </div>
                            )
                        } />

                        <Route path="/admin" element={
                            userRole === 'admin' ? (
                                <div style={{ paddingTop: '6rem' }}><InstitutionalDashboard /></div>
                            ) : (
                                <div className="container" style={{ paddingTop: '10rem', textAlign: 'center' }}>
                                    <h2>Please login as Admin to view institutional data</h2>
                                </div>
                            )
                        } />

                        <Route path="/scam-checker" element={
                            <div style={{ paddingTop: '6rem' }}><ScamChecker /></div>
                        } />
                    </Routes>
                </main>

                <footer className="footer">
                    <div className="container">
                        <p>&copy; 2026 CyberGuard AI. Strengthen your digital immunity.</p>
                    </div>
                </footer>
            </div>
        </Router>
    );
}

export default App;
