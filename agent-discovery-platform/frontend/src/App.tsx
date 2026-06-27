import React, { useState } from 'react';
import { Search, Server, Shield, Brain } from 'lucide-react';
import { FeedbackPanel } from './components/harness/FeedbackPanel';
import { CitationPanel } from './components/harness/CitationPanel';
import { ConfidenceBar } from './components/harness/ConfidenceBar';

function App() {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;
    
    setIsSearching(true);
    
    // Mock API call to backend discovery pipeline
    setTimeout(() => {
      setResults({
        recommended_agents: [
          {
            id: '111-222',
            name: 'Customer Support Agent',
            description: 'Handles customer support queries',
            status: 'PRODUCTION',
            capabilities: ['text_summarization', 'query_routing']
          }
        ],
        citations: [
          {
            source_type: 'agent_registry',
            name: 'Customer Support Agent',
            excerpt: 'Capabilities match: text_summarization, query_routing'
          },
          {
            source_type: 'github',
            name: 'customer-support-agent/README.md',
            excerpt: 'Agent designed for tier 1 support.'
          }
        ],
        confidence: {
          overall: 0.92
        }
      });
      setIsSearching(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="text-blue-600" size={28} />
            <h1 className="text-xl font-bold tracking-tight">Universal Agent Discovery</h1>
          </div>
          <nav className="flex items-center gap-6 text-sm font-medium text-gray-600">
            <a href="#" className="hover:text-blue-600 text-blue-600">Discover</a>
            <a href="#" className="hover:text-blue-600">Marketplace</a>
            <a href="#" className="hover:text-blue-600">Governance</a>
            <a href="#" className="hover:text-blue-600">Analytics</a>
          </nav>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-extrabold text-gray-900 mb-4">Find the right AI Agent for your task</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Search across the enterprise registry, GitHub repositories, and Confluence to discover reusable agents and MCP tools before building your own.
          </p>
        </div>

        <form onSubmit={handleSearch} className="relative shadow-xl rounded-2xl overflow-hidden mb-8">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Search className="h-6 w-6 text-gray-400" />
          </div>
          <input
            type="text"
            className="block w-full pl-12 pr-32 py-5 text-lg border-0 focus:ring-2 focus:ring-blue-500 bg-white"
            placeholder="E.g., I need an agent to summarize release notes from Jira..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <div className="absolute inset-y-0 right-2 flex items-center">
            <button
              type="submit"
              disabled={isSearching}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-xl transition-colors disabled:opacity-50"
            >
              {isSearching ? 'Analyzing...' : 'Discover'}
            </button>
          </div>
        </form>

        {results && (
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h3 className="text-xl font-bold text-gray-900">Recommended Agent</h3>
                <p className="text-sm text-gray-500 mt-1">Based on semantic match and enterprise governance.</p>
              </div>
              <ConfidenceBar score={results.confidence.overall} />
            </div>

            {results.recommended_agents.map((agent: any) => (
              <div key={agent.id} className="border border-blue-100 bg-blue-50/30 rounded-xl p-5">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="text-lg font-semibold text-blue-900">{agent.name}</h4>
                    <p className="text-gray-600 mt-1">{agent.description}</p>
                    
                    <div className="flex gap-2 mt-4">
                      {agent.capabilities.map((cap: string) => (
                        <span key={cap} className="px-2.5 py-1 bg-white border border-gray-200 rounded-md text-xs font-medium text-gray-600">
                          {cap}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center gap-1.5 px-2.5 py-1 bg-green-100 text-green-800 rounded-md text-xs font-bold">
                    <Shield size={14} />
                    {agent.status}
                  </div>
                </div>

                {/* AI Harness UI Components */}
                <CitationPanel citations={results.citations} />
                <FeedbackPanel logId="log-uuid-123" agentId={agent.id} />
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
