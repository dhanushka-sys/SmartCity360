"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

interface TabsProps {
  value: string;
  onValueChange: (value: string) => void;
  items: { value: string; label: string; count?: number; icon?: React.ReactNode }[];
  className?: string;
}

export function Tabs({ value, onValueChange, items, className }: TabsProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center gap-1.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-950/60 p-1.5 backdrop-blur-md shadow-sm",
        className
      )}
    >
      {items.map((item) => {
        const isActive = item.value === value;
        return (
          <button
            key={item.value}
            onClick={() => onValueChange(item.value)}
            className={cn(
              "inline-flex items-center gap-2 rounded-lg px-3.5 py-1.5 text-xs font-medium transition-all duration-200 select-none",
              isActive
                ? "bg-white dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-semibold shadow-sm border border-slate-200 dark:border-slate-700/60"
                : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-200/60 dark:hover:bg-slate-900/60"
            )}
          >
            {item.icon}
            <span>{item.label}</span>
            {item.count !== undefined && (
              <span
                className={cn(
                  "rounded-full px-1.5 py-0.2 text-[10px]",
                  isActive
                    ? "bg-cyan-100 dark:bg-cyan-950 text-cyan-800 dark:text-cyan-300 border border-cyan-200 dark:border-cyan-800"
                    : "bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400"
                )}
              >
                {item.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
