import { useState, FormEvent } from "react";
import { Send, CheckCircle2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

const LEAD_WEBHOOK_URL =
  import.meta.env.VITE_LEAD_WEBHOOK_URL ?? "https://akcegy.app.n8n.cloud/webhook/ai-marketing-lead";

type Status = "idle" | "sending" | "done" | "error";

const LeadForm = () => {
  const [status, setStatus] = useState<Status>("idle");
  const [next, setNext] = useState("");

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const data = Object.fromEntries(new FormData(form).entries());
    if (data.website) return; // honeypot
    delete data.website;
    setStatus("sending");
    try {
      const res = await fetch(LEAD_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...data, source: "website" }),
      });
      if (!res.ok) throw new Error(String(res.status));
      const json = await res.json().catch(() => ({}));
      setNext(json.next ?? "We'll be in touch soon.");
      setStatus("done");
      form.reset();
    } catch {
      setStatus("error");
    }
  };

  if (status === "done") {
    return (
      <div className="glass rounded-xl p-8 text-center max-w-xl mx-auto" role="status">
        <CheckCircle2 className="w-10 h-10 text-primary mx-auto mb-3" />
        <p className="text-xl font-medium">Thank you! {next}</p>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="glass rounded-xl p-6 md:p-8 max-w-xl mx-auto text-left space-y-4">
      <div className="grid sm:grid-cols-2 gap-4">
        <Input name="name" placeholder="Your name" required maxLength={100} aria-label="Your name" />
        <Input name="company" placeholder="Company / store" maxLength={100} aria-label="Company" />
        <Input name="email" type="email" placeholder="Email" required maxLength={150} aria-label="Email" />
        <Input name="phone" type="tel" placeholder="WhatsApp number" maxLength={30} aria-label="WhatsApp number" />
      </div>
      <Textarea
        name="message"
        placeholder="Tell us about your store, monthly ad spend and goals"
        required
        maxLength={1000}
        rows={4}
        aria-label="Message"
      />
      <input name="website" tabIndex={-1} autoComplete="off" className="hidden" aria-hidden="true" />
      <button type="submit" disabled={status === "sending"} className="cta-button w-full inline-flex items-center justify-center gap-2">
        <Send className="w-5 h-5" />
        {status === "sending" ? "Sending…" : "Get My AI Growth Plan"}
      </button>
      {status === "error" && (
        <p className="text-sm text-destructive" role="alert">
          Something went wrong. Please try again or message us on WhatsApp.
        </p>
      )}
    </form>
  );
};

export default LeadForm;
