"use client";

import * as React from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { PolicyCategory, PolicyRule } from "@/types/policy";
import { PoliciesService } from "@/lib/api/policies-service";
import { CheckCircle2, AlertCircle } from "lucide-react";

interface CreatePolicyModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: (policy: PolicyRule) => void;
}

export function CreatePolicyModal({ isOpen, onClose, onCreated }: CreatePolicyModalProps) {
  const [name, setName] = React.useState("");
  const [code, setCode] = React.useState("");
  const [category, setCategory] = React.useState<PolicyCategory>("ENVIRONMENT");
  const [expression, setExpression] = React.useState("NOISE_LEVEL <= 60");
  const [description, setDescription] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");

  const validation = React.useMemo(() => {
    if (!expression.trim()) return { isValid: false, errorMessage: "Expression is empty" };
    return PoliciesService.validateExpression(expression);
  }, [expression]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !expression.trim()) {
      setError("Name and expression are required");
      return;
    }
    if (!validation.isValid) {
      setError(validation.errorMessage || "Invalid syntax in policy expression");
      return;
    }
    setError("");
    setLoading(true);

    try {
      const generatedCode = code.trim() || `POL-${category.slice(0, 3)}-${Math.floor(10 + Math.random() * 90)}`;
      const created = await PoliciesService.createPolicy({
        code: generatedCode,
        name,
        category,
        expression,
        description: description || `Enforces DSL policy rule '${expression}' across active zones.`,
        status: "ACTIVE",
      });

      onCreated(created);
      onClose();
      setName("");
      setExpression("NOISE_LEVEL <= 60");
      setDescription("");
    } catch (err: any) {
      setError(err?.message || "Failed to create policy");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Define City Operational Policy (DSL)"
      description="Define a new domain-specific language rule parsed and executed by the Interpreter Pattern."
      maxWidth="md"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={loading || !validation.isValid}>
            {loading ? "Validating & Compiling AST..." : "Save Policy"}
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Policy Rule Name"
          placeholder="e.g. Waterfront Industrial Acoustic Cap"
          value={name}
          onChange={(e) => setName(e.target.value)}
          error={error}
        />

        <div className="grid grid-cols-2 gap-3">
          <Select
            label="Domain Category"
            value={category}
            onChange={(e) => setCategory(e.target.value as PolicyCategory)}
            options={[
              { label: "Environment & Air", value: "ENVIRONMENT" },
              { label: "Traffic & Transit", value: "TRAFFIC" },
              { label: "Safety & Speed", value: "SAFETY" },
              { label: "Energy & Grid", value: "ENERGY" },
              { label: "Zoning & Curfew", value: "ZONING" },
            ]}
          />
          <Input
            label="Rule Code (Optional)"
            placeholder="e.g. POL-NOISE-WATER"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
        </div>

        <div className="space-y-1.5">
          <label className="block text-xs font-medium text-slate-700 dark:text-slate-300">
            Policy Expression (DSL)
          </label>
          <input
            type="text"
            className="flex h-9 w-full rounded-lg border border-slate-300 dark:border-slate-700/80 bg-white dark:bg-slate-950/80 px-3 py-1.5 font-mono text-xs text-cyan-800 dark:text-cyan-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500/50 shadow-xs"
            value={expression}
            onChange={(e) => setExpression(e.target.value)}
          />

          {/* Validation Feedback */}
          <div className="flex items-center gap-1.5 pt-1 text-[11px]">
            {validation.isValid ? (
              <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
                <CheckCircle2 className="h-3.5 w-3.5" />
                <span>Valid DSL Syntax: AST node parsed successfully.</span>
              </span>
            ) : (
              <span className="flex items-center gap-1 text-rose-600 dark:text-rose-400 font-medium">
                <AlertCircle className="h-3.5 w-3.5" />
                <span>{validation.errorMessage}</span>
              </span>
            )}
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50 p-2.5 text-[11px] text-slate-600 dark:text-slate-400 space-y-1">
          <p className="font-semibold text-slate-800 dark:text-slate-300">Supported Syntax Examples:</p>
          <div className="font-mono text-cyan-700 dark:text-cyan-400 space-y-0.5">
            <p>• NOISE_LEVEL &lt;= 60</p>
            <p>• PARKING_HOUR BETWEEN 08:00 AND 18:00</p>
            <p>• VEHICLE_SPEED &lt;= 40</p>
            <p>• AIR_QUALITY_AQI &lt;= 100 AND NOISE_LEVEL &lt;= 65</p>
          </div>
        </div>
      </form>
    </Modal>
  );
}
