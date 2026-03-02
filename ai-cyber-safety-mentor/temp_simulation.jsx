import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AlertTriangle, Clock, ShieldCheck, Terminal, XCircle, MoreVertical, Smartphone } from 'lucide-react'

const ScamSimulation = ({ onComplete }) => {
    const [step, setStep] = useState('landing')
    const [reactionTime, setReactionTime] = useState(0)
    const [startTime, setStartTime] = useState(0)

    const startTest = () => {
        setStep('simulation')
        setStartTime(Date.now())
    }

    const handleAction = (isMistake) => {
        const timeTaken = (Date.now() - startTime) / 1000
        setReactionTime(timeTaken)
        setStep(isMistake ? 'failed' : 'passed')
    }

    return (
        <div className="simulation-container">
            <AnimatePresence mode="wait">
                {step === 'landing' && (
                    <motion.div
                        key="landing"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="sim-intro glass-card"
                    >
                        <Terminal className="sim-icon" />
                        <h2>Vulnerability Challenge #1</h2>
                        <p>We are about to simulate a common scam. React how you would in real life. Your behavior will be analyzed.</p>
                        <button className="btn-primary" onClick={startTest}>Start Simulation</button>
                    </motion.div>
                )}

                {step === 'simulation' && (
                    <motion.div
                        key="simulation"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="phone-mockup"
                    >
                        <div className="phone-screen">
                            <div className="phone-header">
                                <span>9:41</span>
                                <div className="phone-notch"></div>
                                <Smartphone size={14} />
                            </div>

                            <div className="message-app">
                                <div className="msg-sender">
                                    <span className="avatar-small">S</span>
                                    <div>
                                        <strong>SBI_BANK_KYC</strong>
                                        <p>Now • SMS</p>
                                    </div>
                                    <MoreVertical size={16} />
                                </div>

                                <div className="msg-content glass-card">
                                    <p>URGENT: Your SBI account KYC has expired. Your UPI access will be blocked tonight at 11:59 PM. Please update now to avoid service interruption.</p>
                                    <a href="#" className="scam-link" onClick={() => handleAction(true)}>https://sbi-kyc-verify.com/login</a>
                                </div>

                                <div className="user-actions-row">
                                    <button className="btn-action" onClick={() => handleAction(false)}>Report as Spam</button>
                                    <button className="btn-action secondary" onClick={() => handleAction(false)}>Ignore & Delete</button>
                                </div>
                            </div>
                        </div>
                        <p className="sim-instruction">Click the action you would normally take.</p>
                    </motion.div>
                )}

                {step === 'failed' && (
                    <motion.div
                        key="failed"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="sim-feedback failed glass-card"
                    >
                        <XCircle className="text-danger" size={48} />
                        <h2>Vulnerability Detected!</h2>
                        <div className="feedback-stats">
                            <div className="stat">
                                <span>Reaction Time:</span>
                                <strong>{reactionTime.toFixed(2)}s</strong>
                            </div>
                            <div className="stat">
                                <span>Trigger:</span>
                                <strong className="text-warning">Urgency & Authority</strong>
                            </div>
                        </div>
                        <p>You clicked the link. This was a <strong>Phishing Attack</strong>. In a real scenario, hackers could have stolen your credentials using that fake link.</p>
                        <button className="btn-outline" onClick={onComplete}>Back to Dashboard</button>
                    </motion.div>
                )}

                {step === 'passed' && (
                    <motion.div
                        key="passed"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="sim-feedback passed glass-card"
                    >
                        <ShieldCheck className="text-success" size={48} />
                        <h2>Threat Neutralized</h2>
                        <div className="feedback-stats">
                            <div className="stat">
                                <span>Detection Time:</span>
                                <strong>{reactionTime.toFixed(2)}s</strong>
                            </div>
                            <div className="stat">
                                <span>Immunity Gain:</span>
                                <strong className="text-success">+15 Points</strong>
                            </div>
                        </div>
                        <p>Great job! You recognized the signs of a phishing attempt (Urgency, suspicious URL, and unauthorized sender).</p>
                        <button className="btn-primary" onClick={onComplete}>Next Challenge</button>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    )
}

export default ScamSimulation
