import React from 'react';
import { FileText, Github, Database } from 'lucide-react';

interface Citation {
  source_id: string;
  source_type: string; // mcp, github, confluence, agent_registry
  name: string;
  excerpt: string;
}

interface CitationPanelProps {
  citations: Citation[];
}

export function CitationPanel({ citations }: CitationPanelProps) {
  if (!citations || citations.length === 0) return null;

  const getIcon = (type: string) => {
    switch (type) {
      case 'github': return <Github size={16} className="text-gray-700" />;
      case 'confluence': return <FileText size={16} className="text-blue-500" />;
      case 'agent_registry': return <Database size={16} className="text-green-600" />;
      default: return <FileText size={16} />;
    }
  };

  return (
    <div className="mt-4 bg-gray-50 p-4 rounded-lg border border-gray-100">
      <h4 className="text-sm font-semibold text-gray-700 mb-2">Sources & Evidence</h4>
      <div className="space-y-3">
        {citations.map((cite, i) => (
          <div key={i} className="flex items-start gap-2 text-sm">
            <div className="mt-0.5">{getIcon(cite.source_type)}</div>
            <div>
              <span className="font-medium text-gray-800">{cite.name}</span>
              <p className="text-gray-500 text-xs mt-1 italic border-l-2 border-gray-300 pl-2">"{cite.excerpt}"</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
