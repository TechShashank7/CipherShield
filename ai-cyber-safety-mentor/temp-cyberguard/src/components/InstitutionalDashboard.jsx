import React from 'react';
import { Users, AlertOctagon, TrendingDown, BookOpen, ChevronRight, Activity, ShieldAlert, BarChart3 } from 'lucide-react';
import { motion } from 'framer-motion';

const InstitutionalDashboard = () => {
    const departments = [
        { name: 'Engineering', members: 120, avgScore: 45, status: 'Improving' },
        { name: 'Marketing', members: 45, avgScore: 72, status: 'High Risk' },
        { name: 'HR/Admin', members: 20, avgScore: 68, status: 'At Risk' },
        { name: 'Sales', members: 85, avgScore: 55, status: 'Stable' },
    ];

    return (
        <div className="dashboard-page admin-dashboard">
            <div className="container">

                <div className="dashboard-header">
                    <div>
                        <h2 className="section-title">Institutional <span className="gradient-text">Overview</span></h2>
                        <p className="text-muted">Global Cyber Health Index for Acme Corp</p>
                    </div>
                    <button className="btn-primary">Launch Mass Simulation Test</button>
                </div>

                <div className="stats-grid">
                    <motion.div className="glass-card stat-box" whileHover={{ y: -5 }}>
                        <div className="stat-icon-wrapper blue-bg"><Users size={24} /></div>
                        <div className="stat-info">
                            <p className="text-muted">Active Users</p>
                            <h3>270</h3>
                        </div>
                    </motion.div>
                    <motion.div className="glass-card stat-box" whileHover={{ y: -5 }}>
                        <div className="stat-icon-wrapper danger-bg"><AlertOctagon size={24} /></div>
                        <div className="stat-info">
                            <p className="text-muted">Overall Vulnerability</p>
                            <h3>58/100</h3>
                        </div>
                    </motion.div>
                    <motion.div className="glass-card stat-box" whileHover={{ y: -5 }}>
                        <div className="stat-icon-wrapper purple-bg"><BarChart3 size={24} /></div>
                        <div className="stat-info">
                            <p className="text-muted">Simulations Run</p>
                            <h3>1,402</h3>
                        </div>
                    </motion.div>
                    <motion.div className="glass-card stat-box" whileHover={{ y: -5 }}>
                        <div className="stat-icon-wrapper green-bg"><TrendingDown size={24} /></div>
                        <div className="stat-info">
                            <p className="text-muted">Weekly Improvement</p>
                            <h3 className="text-success">+14%</h3>
                        </div>
                    </motion.div>
                </div>

                <div className="dashboard-grid admin-main-grid" style={{ marginTop: '2rem' }}>

                    <div className="glass-card deps-card" style={{ gridColumn: 'span 1' }}>
                        <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <Activity size={20} className="text-accent" /> Department Vulnerability
                        </h3>
                        <div className="deps-list">
                            {departments.map((dep, i) => (
                                <div key={i} className="dep-item">
                                    <div className="dep-details">
                                        <h4>{dep.name}</h4>
                                        <span className="text-muted">{dep.members} Members</span>
                                    </div>
                                    <div className="dep-risk">
                                        <div className="progress-bar-bg">
                                            <div
                                                className="progress-fill"
                                                style={{
                                                    width: `${dep.avgScore}%`,
                                                    background: dep.avgScore > 60 ? '#ff4d6d' : (dep.avgScore > 40 ? '#ff8a5c' : '#00f5d4')
                                                }}
                                            ></div>
                                        </div>
                                        <span className="score">{dep.avgScore}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="glass-card insights-card" style={{ gridColumn: 'span 1' }}>
                        <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <ShieldAlert size={20} className="text-warning" /> Critical Insights
                        </h3>
                        <div className="insight-item danger">
                            <p><strong>Marketing Dept</strong> has a 62% failure rate on <em>Urgency</em> simulations this week.</p>
                            <button className="btn-action-small">Assign Training</button>
                        </div>
                        <div className="insight-item warning">
                            <p>15 Employees clicked a simulated Phishing link from an external executive impersonator.</p>
                            <button className="btn-action-small">View Report</button>
                        </div>
                        <div className="insight-item info">
                            <p><strong>Engineering Dept</strong> showed a 20% improvement in detection time.</p>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default InstitutionalDashboard;
