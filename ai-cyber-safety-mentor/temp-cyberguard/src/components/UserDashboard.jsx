import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, AlertTriangle } from 'lucide-react';

const UserDashboard = () => {
    return (
        <div className="dashboard-page">
            <div className="container">
                <div className="dashboard-grid">
                    <div className="glass-card profile-card" style={{ gridColumn: 'span 1' }}>
                        <div className="user-info">
                            <div className="avatar">JD</div>
                            <div>
                                <h2>John Doe</h2>
                                <p className="text-muted">Safety Level: <span className="text-warning">Intermediate</span></p>
                            </div>
                        </div>
                        <div className="score-widget">
                            <div className="circular-progress">
                                <span className="score-num">42</span>
                                <span className="score-label">Risk Score</span>
                            </div>
                            <p className="status-good"><CheckCircle2 size={16} /> Improving Trend</p>
                        </div>
                    </div>

                    <div className="glass-card task-card" style={{ gridColumn: 'span 1' }}>
                        <h3>Active Quests & Simulations</h3>
                        <div className="sim-list">
                            <div className="sim-item">
                                <div className="sim-info">
                                    <AlertTriangle className="text-warning" size={24} />
                                    <div>
                                        <h4>Pending Phishing Test</h4>
                                        <p className="text-muted">Wait for a simulated message on your phone.</p>
                                    </div>
                                </div>
                                <span className="badge-blue">Running</span>
                            </div>
                        </div>
                    </div>

                    <div className="glass-card analytics-card" style={{ gridColumn: 'span 2' }}>
                        <h3>Vulnerability Heatmap</h3>
                        <p className="text-muted">AI-detected mental triggers making you susceptible to attacks.</p>

                        <div className="heatmap-placeholder">
                            <div className="bar-groups">
                                <div className="bar-group">
                                    <div className="bar" style={{ height: '80%' }}></div>
                                    <span>Urgency</span>
                                </div>
                                <div className="bar-group">
                                    <div className="bar" style={{ height: '40%' }}></div>
                                    <span>Greed</span>
                                </div>
                                <div className="bar-group">
                                    <div className="bar" style={{ height: '20%' }}></div>
                                    <span>Fear</span>
                                </div>
                                <div className="bar-group">
                                    <div className="bar" style={{ height: '90%' }}></div>
                                    <span>Authority</span>
                                </div>
                            </div>
                            <div className="heatmap-insights" style={{ marginTop: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                                <span className="badge-small danger-badge">High Risk: Authority</span>
                                <span className="badge-small danger-badge">High Risk: Urgency</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UserDashboard;
