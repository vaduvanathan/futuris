import React, { useState } from 'react';
import { DebateResult, DebateTurn } from '../types';

const DebateInterface: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DebateResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8080/api/debate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: topic }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch debate results');
      }

      const data: DebateResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="debate-container">
      <h1>LLM Debate Arena</h1>
      
      <form onSubmit={handleSubmit} className="debate-form">
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter a debate topic (e.g., 'Is AI conscious?')"
          disabled={loading}
          className="topic-input"
        />
        <button type="submit" disabled={loading} className="start-btn">
          {loading ? 'Debating...' : 'Start Debate'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {loading && (
        <div className="loading-indicator">
          <p>The agents are debating... This may take a minute.</p>
          <div className="spinner"></div>
        </div>
      )}

      {result && (
        <div className="results-area">
          <div className="transcript-section">
            <h2>Debate Transcript</h2>
            <div className="transcript">
              {result.transcript.map((turn, index) => (
                <div key={index} className={`turn ${turn.speaker.replace(' ', '-').toLowerCase()}`}>
                  <h3>{turn.speaker}</h3>
                  <div className="turn-content">{turn.content}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="verdict-section">
            <h2>Judge's Verdict</h2>
            <div className="verdict-card">
              <div className="winner">Winner: <strong>{result.winner}</strong></div>
              <div className="confidence">Confidence: {result.confidence}%</div>
              <div className="reason">"{result.reason}"</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DebateInterface;
