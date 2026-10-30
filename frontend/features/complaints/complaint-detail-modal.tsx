"use client";

import * as React from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { CitizenComplaint, HandlerRole } from "@/types/complaint";
import { ComplaintsService } from "@/lib/api/complaints-service";
import { EscalationTimeline } from "@/features/complaints/escalation-timeline";
import { ArrowUpRight, CheckCircle2, MessageSquare, Send } from "lucide-react";
import { formatDate } from "@/lib/utils";
import { useAppMode } from "@/components/mode-provider";

interface ComplaintDetailModalProps {
  isOpen: boolean;
  onClose: () => void;
  complaint: CitizenComplaint;
  onUpdated: (updated: CitizenComplaint) => void;
}

export function ComplaintDetailModal({
  isOpen,
  onClose,
  complaint,
  onUpdated,
}: ComplaintDetailModalProps) {
  const { isAcademic } = useAppMode();
  const [escalateReason, setEscalateReason] = React.useState("");
  const [newNote, setNewNote] = React.useState("");
  const [resolveSummary, setResolveSummary] = React.useState("");
  const [showEscalateForm, setShowEscalateForm] = React.useState(false);
  const [showResolveForm, setShowResolveForm] = React.useState(false);
  const [loading, setLoading] = React.useState(false);

  const canEscalate =
    complaint.status !== "RESOLVED" && complaint.currentHandlerRole !== "CITY_MANAGER";

  const handleEscalate = async () => {
    if (!escalateReason.trim()) return;
    setLoading(true);
    try {
      const updated = await ComplaintsService.escalateComplaint(complaint.id, escalateReason);
      onUpdated(updated);
      setShowEscalateForm(false);
      setEscalateReason("");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddNote = async () => {
    if (!newNote.trim()) return;
    setLoading(true);
    try {
      const updated = await ComplaintsService.addNote(
        complaint.id,
        newNote,
        "Elena Rostova",
        complaint.currentHandlerRole
      );
      onUpdated(updated);
      setNewNote("");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleResolve = async () => {
    if (!resolveSummary.trim()) return;
    setLoading(true);
    try {
      const updated = await ComplaintsService.resolveComplaint(complaint.id, resolveSummary);
      onUpdated(updated);
      setShowResolveForm(false);
      setResolveSummary("");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Complaint ${complaint.trackingNumber}`}
      description={`Reported incident in ${complaint.zoneName}`}
      maxWidth="3xl"
      footer={
        <div className="flex items-center justify-between w-full">
          <span className="text-[11px] text-slate-500 dark:text-slate-400">
            {isAcademic
              ? "Chain of Responsibility Pattern Handler Evaluation"
              : "Municipal Incident Resolution Protocol"}
          </span>
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
        </div>
      }
    >
      <div className="space-y-6 text-xs">
        {/* Header Summary */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-4 space-y-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white">{complaint.title}</h3>
            <div className="flex items-center gap-2">
              <Badge
                variant={
                  complaint.severity === "CRITICAL"
                    ? "danger"
                    : complaint.severity === "HIGH"
                    ? "warning"
                    : "default"
                }
                dot
              >
                {complaint.severity}
              </Badge>
              <Badge variant="blue">{complaint.category}</Badge>
              <Badge
                variant={complaint.status === "RESOLVED" ? "success" : "purple"}
              >
                {complaint.status}
              </Badge>
            </div>
          </div>
          <p className="text-slate-700 dark:text-slate-300 leading-relaxed text-xs">{complaint.description}</p>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-slate-200 dark:border-slate-800/80 text-[11px]">
            <div>
              <span className="text-slate-500 dark:text-slate-400">Reporter:</span>
              <p className="font-semibold text-slate-900 dark:text-white mt-0.5">{complaint.citizenName}</p>
            </div>
            <div>
              <span className="text-slate-500 dark:text-slate-400">Contact:</span>
              <p className="font-mono text-slate-700 dark:text-slate-300 mt-0.5">{complaint.citizenContact}</p>
            </div>
            <div>
              <span className="text-slate-500 dark:text-slate-400">Current Assigned Handler:</span>
              <p className="font-semibold text-cyan-700 dark:text-cyan-300 mt-0.5">
                {complaint.currentHandlerRole.replace("_", " ")}
              </p>
            </div>
            <div>
              <span className="text-slate-500 dark:text-slate-400">Logged At:</span>
              <p className="text-slate-700 dark:text-slate-300 mt-0.5">{formatDate(complaint.submittedAt)}</p>
            </div>
          </div>
        </div>

        {/* Action Triggers */}
        {complaint.status !== "RESOLVED" && (
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-950/40 p-3.5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                Handler Workflow Actions
              </span>
              <span className="text-[10px] text-cyan-700 dark:text-cyan-400 font-medium">
                Current Tier: {complaint.currentHandlerRole.replace("_", " ")}
              </span>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              {canEscalate && (
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setShowEscalateForm(!showEscalateForm)}
                  className="gap-1.5 text-xs text-amber-700 dark:text-amber-400 hover:text-amber-800 dark:hover:text-amber-300 hover:border-amber-300 dark:hover:border-amber-500/50"
                >
                  <ArrowUpRight className="h-3.5 w-3.5" />
                  <span>Escalate Along Chain</span>
                </Button>
              )}

              <Button
                size="sm"
                variant="outline"
                onClick={() => setShowResolveForm(!showResolveForm)}
                className="gap-1.5 text-xs text-emerald-700 dark:text-emerald-400 hover:text-emerald-800 dark:hover:text-emerald-300 hover:border-emerald-300 dark:hover:border-emerald-500/50"
              >
                <CheckCircle2 className="h-3.5 w-3.5" />
                <span>Mark Ticket Resolved</span>
              </Button>
            </div>

            {/* Escalate Drawer Form */}
            {showEscalateForm && (
              <div className="rounded-xl border border-amber-200 dark:border-amber-900/40 bg-amber-50 dark:bg-amber-950/20 p-3 space-y-2">
                <p className="font-semibold text-amber-900 dark:text-amber-200 text-xs">
                  Escalate to Next Chain Handler (
                  {complaint.currentHandlerRole === "LOCAL_STAFF" ? "Supervisor" : "City Manager"})
                </p>
                <Input
                  placeholder="Enter specific justification for promoting ticket..."
                  value={escalateReason}
                  onChange={(e) => setEscalateReason(e.target.value)}
                  className="text-xs"
                />
                <div className="flex justify-end gap-2 pt-1">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setShowEscalateForm(false)}
                  >
                    Cancel
                  </Button>
                  <Button
                    size="sm"
                    variant="warning"
                    onClick={handleEscalate}
                    disabled={loading || !escalateReason.trim()}
                  >
                    Confirm Forward
                  </Button>
                </div>
              </div>
            )}

            {/* Resolve Drawer Form */}
            {showResolveForm && (
              <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/40 bg-emerald-50 dark:bg-emerald-950/20 p-3 space-y-2">
                <p className="font-semibold text-emerald-900 dark:text-emerald-200 text-xs">
                  Resolve and Close Incident Ticket
                </p>
                <Input
                  placeholder="Provide resolution summary (actions taken, contractor dispatched, etc.)..."
                  value={resolveSummary}
                  onChange={(e) => setResolveSummary(e.target.value)}
                  className="text-xs"
                />
                <div className="flex justify-end gap-2 pt-1">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setShowResolveForm(false)}
                  >
                    Cancel
                  </Button>
                  <Button
                    size="sm"
                    variant="default"
                    onClick={handleResolve}
                    disabled={loading || !resolveSummary.trim()}
                  >
                    Close Complaint
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Resolved Notice if applicable */}
        {complaint.status === "RESOLVED" && complaint.resolutionSummary && (
          <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/50 bg-emerald-50 dark:bg-emerald-950/20 p-3.5 text-xs text-emerald-800 dark:text-emerald-300">
            <div className="flex items-center gap-2 font-semibold text-emerald-900 dark:text-emerald-200">
              <CheckCircle2 className="h-4 w-4" />
              <span>Resolved at {formatDate(complaint.resolvedAt || "")}</span>
            </div>
            <p className="mt-1 text-[11px] text-slate-700 dark:text-slate-300">{complaint.resolutionSummary}</p>
          </div>
        )}

        {/* Escalation Path Timeline */}
        <EscalationTimeline
          history={complaint.escalationHistory}
          currentRole={complaint.currentHandlerRole}
        />

        {/* Internal Notes / Log */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
              Internal Handler Notes ({complaint.notes.length})
            </h4>
          </div>

          <div className="space-y-2 max-h-40 overflow-y-auto">
            {complaint.notes.map((note) => (
              <div
                key={note.id}
                className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50 p-2.5 text-xs space-y-1"
              >
                <div className="flex items-center justify-between text-[10px] text-slate-500 dark:text-slate-400">
                  <span className="font-semibold text-slate-800 dark:text-slate-200">
                    {note.author} ({note.role.replace("_", " ")})
                  </span>
                  <span className="font-mono">{formatDate(note.createdAt)}</span>
                </div>
                <p className="text-slate-700 dark:text-slate-300 text-[11px]">{note.text}</p>
              </div>
            ))}
          </div>

          {complaint.status !== "RESOLVED" && (
            <div className="flex items-center gap-2 pt-1">
              <Input
                placeholder="Append operational note..."
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                className="text-xs h-8"
              />
              <Button
                size="sm"
                variant="secondary"
                onClick={handleAddNote}
                disabled={loading || !newNote.trim()}
                className="h-8 gap-1 text-xs"
              >
                <Send className="h-3 w-3" />
                <span>Add</span>
              </Button>
            </div>
          )}
        </div>
      </div>
    </Modal>
  );
}
