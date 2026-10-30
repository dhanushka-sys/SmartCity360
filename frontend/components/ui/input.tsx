import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, label, error, hint, id, ...props }, ref) => {
    const inputId = id || React.useId();
    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label htmlFor={inputId} className="block text-xs font-medium text-slate-700 dark:text-slate-300">
            {label}
          </label>
        )}
        <input
          id={inputId}
          type={type}
          className={cn(
            "flex h-9 w-full rounded-lg border border-slate-300 dark:border-slate-700/80 bg-white dark:bg-slate-950/60 px-3 py-1.5 text-sm text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500/50 focus-visible:border-cyan-500 disabled:cursor-not-allowed disabled:opacity-50 transition-all shadow-sm",
            error && "border-rose-500 focus-visible:ring-rose-500/50",
            className
          )}
          ref={ref}
          {...props}
        />
        {hint && !error && <p className="text-[11px] text-slate-500 dark:text-slate-400">{hint}</p>}
        {error && <p className="text-[11px] text-rose-600 dark:text-rose-400 font-medium">{error}</p>}
      </div>
    );
  }
);
Input.displayName = "Input";
