"use client";

import * as React from "react";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ComplaintsService } from "@/lib/api/complaints-service";
import { CitizenComplaint } from "@/types/complaint";

export function RecentComplaintsTable() {
  const [complaints, setComplaints] = React.useState<CitizenComplaint[]>([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    let mounted = true;
    ComplaintsService.getComplaints()
      .then((data) => {
        if (mounted) setComplaints(data.slice(0, 5));
      })
      .catch(() => {
        if (mounted) setComplaints([]);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between pb-3">
        <div>
          <CardTitle className="text-sm md:text-base">Recent Incident Escalations</CardTitle>
          <CardDescription>
            Live status from MySQL citizen complaints
          </CardDescription>
        </div>
        <Link
          href="/complaints"
          className="flex items-center gap-1 text-xs font-semibold text-cyan-600 dark:text-cyan-400 hover:text-cyan-700 dark:hover:text-cyan-300 transition-colors"
        >
          <span>View All ({complaints.length})</span>
          <ArrowUpRight className="h-3.5 w-3.5" />
        </Link>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          {loading ? (
            <div className="text-center py-6 text-xs text-slate-500">Loading complaints from database...</div>
          ) : complaints.length === 0 ? (
            <div className="text-center py-6 text-xs text-slate-500">No complaints found. Ensure Tomcat 9 is running.</div>
          ) : (
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  <th className="pb-2.5">ID</th>
                  <th className="pb-2.5">Title &amp; Zone</th>
                  <th className="pb-2.5">Severity</th>
                  <th className="pb-2.5">Current Role</th>
                  <th className="pb-2.5">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                {complaints.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                    <td className="py-2.5 font-mono text-slate-700 dark:text-slate-300">{c.trackingNumber || c.id}</td>
                    <td className="py-2.5 pr-2 max-w-[200px]">
                      <p className="font-medium text-slate-900 dark:text-white truncate">{c.title}</p>
                      <p className="text-[10px] text-slate-500 dark:text-slate-400">{c.zoneName}</p>
                    </td>
                    <td className="py-2.5">
                      <Badge
                        variant={
                          c.severity === "CRITICAL"
                            ? "danger"
                            : c.severity === "HIGH"
                            ? "warning"
                            : c.severity === "MEDIUM"
                            ? "info"
                            : "default"
                        }
                        dot
                      >
                        {c.severity}
                      </Badge>
                    </td>
                    <td className="py-2.5 text-slate-700 dark:text-slate-300 font-medium">
                      <span className="rounded bg-slate-100 dark:bg-slate-800 px-2 py-0.5 text-[10px] text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700/60">
                        {c.currentHandlerRole.replace("_", " ")}
                      </span>
                    </td>
                    <td className="py-2.5">
                      <span
                        className={`text-[11px] font-semibold ${
                          c.status === "RESOLVED"
                            ? "text-emerald-600 dark:text-emerald-400"
                            : c.status === "ESCALATED"
                            ? "text-rose-600 dark:text-rose-400"
                            : "text-amber-600 dark:text-amber-400"
                        }`}
                      >
                        {c.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
