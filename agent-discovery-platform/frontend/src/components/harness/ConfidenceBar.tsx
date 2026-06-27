import React from 'react';
import { ShieldCheck, ShieldAlert } from 'lucide-react';

interface ConfidenceBarProps {
  score: number; // 0.0 to 1.0
  factors?: string[];
}

export function ConfidenceBar({ score, factors = [] }: ConfidenceBarProps) {
  const percentage = Math.round(score * 100);
  
  let color = "bg-green-500";
  let textColor = "text-green-700";
  let icon = <ShieldCheck size={16} className="text-green-600" />;
  
  if (score < 0.6) {
    color = "bg-red-500";
    textColor = "text-red-700";
    icon = <ShieldAlert size={16} className="text-red-600" />;
  } else if (score < 0.85) {
    color = "bg-yellow-500";
    textColor = "text-yellow-700";
    icon = <ShieldCheck size={16} className="text-yellow-600" />;
  }

  return (
    <div className="flex items-center gap-3">
      <div className="flex items-center gap-1">
        {icon}
        <span className={`text-xs font-bold ${textColor}`}>
          {percentage}% Match Confidence
        </span>
      </div>
      <div className="h-2 w-32 bg-gray-200 rounded-full overflow-hidden">
        <div 
          className={`h-full ${color} transition-all duration-500`} 
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
