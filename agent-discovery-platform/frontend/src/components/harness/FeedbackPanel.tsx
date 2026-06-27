import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown, MessageSquare } from 'lucide-react';

interface FeedbackPanelProps {
  logId: string;
  agentId?: string;
}

export function FeedbackPanel({ logId, agentId }: FeedbackPanelProps) {
  const [status, setStatus] = useState<'idle' | 'submitted'>('idle');

  const handleFeedback = async (type: 'thumbs_up' | 'thumbs_down') => {
    // Mock API Call to /api/v1/feedback
    console.log(`Submitting ${type} for log ${logId}`);
    setStatus('submitted');
  };

  if (status === 'submitted') {
    return <div className="text-sm text-green-600 font-medium">Thank you for your feedback! This helps improve recommendations.</div>;
  }

  return (
    <div className="flex items-center gap-4 border-t pt-3 mt-4">
      <span className="text-sm text-gray-500 font-medium">Was this recommendation helpful?</span>
      <button 
        onClick={() => handleFeedback('thumbs_up')}
        className="flex items-center gap-1 text-gray-500 hover:text-green-600 transition-colors"
        title="Good recommendation"
      >
        <ThumbsUp size={18} />
      </button>
      <button 
        onClick={() => handleFeedback('thumbs_down')}
        className="flex items-center gap-1 text-gray-500 hover:text-red-600 transition-colors"
        title="Poor recommendation"
      >
        <ThumbsDown size={18} />
      </button>
      <button 
        className="flex items-center gap-1 text-sm text-blue-500 hover:text-blue-700 font-medium ml-auto"
      >
        <MessageSquare size={16} />
        Suggest Correction
      </button>
    </div>
  );
}
