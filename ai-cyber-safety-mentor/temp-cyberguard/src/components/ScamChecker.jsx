import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Info, AlertTriangle, ShieldAlert, CheckCircle2, ShieldCheck } from 'lucide-react';

const ScamChecker = () => {
    const [message, setMessage] = useState('');
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [result, setResult] = useState(null);

    const analyzeMessage = () => {
        if (!message.trim()) return;
        setIsAnalyzing(true);
        setResult(null);

        // Simulate AI analysis delay
        setTimeout(() => {
            setIsAnalyzing(false);

            const isScam = message.toLowerCase().includes('congratulations') ||
                message.toLowerCase().includes('lakh') ||
                message.toLowerCase().includes('urgent') ||
                message.toLowerCase().includes('kyc');

            setResult({
                scamProbability: isScam ? 94 : 15,
                category: isScam ? 'Lottery / Financial Fraud' : 'Safe / Low Threat',
                triggers: isScam ? ['Greed Trigger', 'Urgency Pressure', 'False Reward'] : ['None Detected'],
                confidence: 98,
                description: isScam
                    ? "This message uses classic 'Too Good to be True' tactics mixed with urgency. Scammers use this to bypass your logical thinking and force a quick action."
                    : "This message doesn't contain common trigger words used by cybercriminals. However, always verify the sender if it includes links."
            });
        }, 2500);
    };

    return (
        <div className="scam-checker-page dashboard-page">
            <div className="container">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card checker-container"
                >
                    <h2 className="section-title text-center">AI Scam <span className="gradient-text">Detector</span></h2>
                    <p className="text-center text-muted">Paste a suspicious message below and our AI will analyze its psychological triggers.</p>

                    <div className="input-group">
                        <textarea
                            placeholder="Paste message here... e.g., 'Congratulations! You won ₹5 lakh. Click below to claim.'"
                            className="scam-textarea"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                        ></textarea>
                        <button
                            className="btn-primary checker-btn"
                            onClick={analyzeMessage}
                            disabled={isAnalyzing}
                        >
                            <Search size={20} />
                            {isAnalyzing ? 'Analyzing Patterns...' : 'Analyze Now'}
                        </button>
                    </div>

                    <div className="checker-result-placeholder">
                        {!result && !isAnalyzing && (
                            <div className="result-item default-state">
                                <div className="info-icon"><Info size={24} /></div>
                                <div>
                                    <h4>Analyze patterns of fraud securely</h4>
                                    <p>We check for UPI fraud, OTP scams, fake KYC, and behavioral manipulation.</p>
                                </div>
                            </div>
                        )}

                        {isAnalyzing && (
                            <div className="scanning-animation text-center">
                                <div className="scanner-line"></div>
                                <motion.p
                                    animate={{ opacity: [0.5, 1, 0.5] }}
                                    transition={{ repeat: Infinity, duration: 1.5 }}
                                    style={{ color: 'var(--primary)', marginTop: '2rem' }}
                                >
                                    Running heuristic analysis & psychological profiling...
                                </motion.p>
                            </div>
                        )}

                        {result && (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="analysis-results"
                            >
                                <div className={`result-header ${result.scamProbability > 50 ? 'danger-bg' : 'success-bg'}`}>
                                    {result.scamProbability > 50 ? <ShieldAlert size={32} /> : <ShieldCheck size={32} />}
                                    <div>
                                        <h3>{result.scamProbability > 50 ? 'High Risk Detected' : 'Looks Safe'}</h3>
                                        <p>{result.scamProbability}% Scam Probability</p>
                                    </div>
                                </div>

                                <div className="result-details">
                                    <div className="detail-item glass-card">
                                        <span className="text-muted">Category</span>
                                        <strong>{result.category}</strong>
                                    </div>
                                    <div className="detail-item glass-card">
                                        <span className="text-muted">AI Confidence</span>
                                        <strong>{result.confidence}%</strong>
                                    </div>
                                </div>

                                <div className="triggers-list glass-card">
                                    <span className="text-muted" style={{ display: 'block', marginBottom: '1rem' }}>Detected Psychological Triggers:</span>
                                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                                        {result.triggers.map((trigger, i) => (
                                            <span key={i} className={`badge-small ${result.scamProbability > 50 ? 'danger-badge' : 'success-badge'}`}>
                                                {trigger}
                                            </span>
                                        ))}
                                    </div>
                                    <p style={{ marginTop: '1.5rem', lineHeight: '1.6' }}>{result.description}</p>
                                </div>
                            </motion.div>
                        )}
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default ScamChecker;
