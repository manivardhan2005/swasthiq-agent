import React from 'react';
import { Link } from 'react-router-dom';

const ConversationDetail = () => {
  return (
    <div className="max-w-[1100px] mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-[#003C89] mb-1">2. Conversation Detail</h1>
      </div>

      <div className="bg-white rounded-xl border border-[#E4E7EC] shadow-sm mb-8 overflow-hidden">
        <div className="p-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h2 className="text-xl font-bold text-[#101828]">Conversation cv_4471</h2>
              <p className="text-sm text-[#475467] mt-1">Sunrise Clinic, Dehradun — 27 Sep 2026, 11:42</p>
            </div>
            <span className="inline-flex items-center px-3 py-1 rounded text-xs font-bold bg-red-50 text-red-700 tracking-wider">
              ESCALATED — CLINICAL
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <div className="border border-[#E4E7EC] rounded-lg p-5">
                <h3 className="text-sm font-bold text-[#101828] mb-5">Transcript and tool calls</h3>
                
                <div className="space-y-6">
                  {/* Turn 1 */}
                  <div className="flex gap-4">
                    <div className="text-xs font-bold text-[#475467] tracking-wider w-16 pt-2 shrink-0">CALLER</div>
                    <div className="bg-[#F8F9FB] border border-[#E4E7EC] rounded-lg p-3 text-sm text-[#101828] w-full max-w-[80%]">
                      Kal subah ka appointment mil jayega Dr. Rao ke saath?
                    </div>
                  </div>
                  
                  {/* Tool Call 1 */}
                  <div className="flex gap-4">
                    <div className="text-xs font-bold text-[#475467] tracking-wider w-16 pt-2 shrink-0">TOOL</div>
                    <div className="bg-blue-50 border border-blue-100 rounded-lg p-3 text-xs font-mono text-blue-900 w-full max-w-[80%]">
                      <span className="font-bold">search_slots</span>(doctor_id="d_rao", date="2026-09-28", window="morning")<br/>
                      <span className="text-blue-600">→ 3 slots: 09:30, 10:15, 11:00</span>
                    </div>
                  </div>
                  
                  {/* Agent 1 */}
                  <div className="flex gap-4">
                    <div className="text-xs font-bold text-[#475467] tracking-wider w-16 pt-2 shrink-0">AGENT</div>
                    <div className="border border-[#E4E7EC] rounded-lg p-3 text-sm text-[#101828] w-full max-w-[80%]">
                      Ji, kal subah 9:30, 10:15 aur 11:00 khali hai. Kaun sa theek rahega?
                    </div>
                  </div>
                  
                  {/* Turn 2 */}
                  <div className="flex gap-4">
                    <div className="text-xs font-bold text-[#475467] tracking-wider w-16 pt-2 shrink-0">CALLER</div>
                    <div className="bg-[#F8F9FB] border border-[#E4E7EC] rounded-lg p-3 text-sm text-[#101828] w-full max-w-[80%]">
                      10:15 kar dijiye. Waise abhi seene mein dard ho raha hai thoda.
                    </div>
                  </div>
                  
                  {/* Tool Call 2 */}
                  <div className="flex gap-4">
                    <div className="text-xs font-bold text-[#475467] tracking-wider w-16 pt-2 shrink-0">TOOL</div>
                    <div className="bg-blue-50 border border-blue-100 rounded-lg p-3 text-xs font-mono text-blue-900 w-full max-w-[80%]">
                      <span className="font-bold">escalate_to_human</span>(reason="clinical_urgent",<br/>
                      &nbsp;&nbsp;detail="caller reports active chest pain")
                    </div>
                  </div>
                  
                  {/* Agent 2 */}
                  <div className="flex gap-4">
                    <div className="text-xs font-bold text-[#475467] tracking-wider w-16 pt-2 shrink-0">AGENT</div>
                    <div className="border border-[#E4E7EC] rounded-lg p-3 text-sm text-[#101828] w-full max-w-[80%]">
                      Main abhi aapko clinic se connect kar rahi hoon. Agar dard badh raha hai, turant nazdeeki emergency par jaiye.
                    </div>
                  </div>
                  
                  {/* Outcome Alert */}
                  <div className="flex gap-4 mt-8">
                    <div className="w-16 shrink-0"></div>
                    <div className="bg-red-50 text-red-700 text-sm font-semibold rounded px-4 py-3 border border-red-200">
                      Booking flow abandoned. No appointment was created.
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="lg:col-span-1">
              <div className="border border-[#E4E7EC] rounded-lg p-5">
                <h3 className="text-sm font-bold text-[#101828] mb-5">Outcome</h3>
                
                <table className="w-full text-sm">
                  <tbody>
                    <tr className="border-b border-[#E4E7EC]">
                      <td className="py-3 text-[#475467]">terminal_state</td>
                      <td className="py-3 text-right font-mono font-medium text-[#101828]">escalated</td>
                    </tr>
                    <tr className="border-b border-[#E4E7EC]">
                      <td className="py-3 text-[#475467]">escalation_reason</td>
                      <td className="py-3 text-right font-mono font-medium text-[#101828]">clinical_urgent</td>
                    </tr>
                    <tr className="border-b border-[#E4E7EC]">
                      <td className="py-3 text-[#475467]">patient_id</td>
                      <td className="py-3 text-right font-mono font-medium text-[#101828]">pt_0192</td>
                    </tr>
                    <tr className="border-b border-[#E4E7EC]">
                      <td className="py-3 text-[#475467]">appointment_id</td>
                      <td className="py-3 text-right font-mono font-medium text-[#101828]">null</td>
                    </tr>
                    <tr className="border-b border-[#E4E7EC]">
                      <td className="py-3 text-[#475467]">tool_calls</td>
                      <td className="py-3 text-right font-mono font-medium text-[#101828]">2</td>
                    </tr>
                    <tr className="border-b border-[#E4E7EC]">
                      <td className="py-3 text-[#475467]">turns</td>
                      <td className="py-3 text-right font-mono font-medium text-[#101828]">6</td>
                    </tr>
                    <tr className="border-b border-[#E4E7EC]">
                      <td className="py-3 text-[#475467]">tokens</td>
                      <td className="py-3 text-right font-mono font-medium text-[#101828]">3,140</td>
                    </tr>
                    <tr className="border-b border-[#E4E7EC]">
                      <td className="py-3 text-[#475467]">latency</td>
                      <td className="py-3 text-right font-mono font-medium text-[#101828]">4.2 s</td>
                    </tr>
                  </tbody>
                </table>
                
                <div className="mt-5">
                  <div className="text-[10px] font-bold text-[#475467] tracking-wider mb-2 uppercase">Determinism</div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#475467]">Same terminal state across 3 runs.</span>
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-green-50 text-green-700">
                      STABLE
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="text-center text-sm text-[#475467] italic mt-8 max-w-2xl mx-auto leading-relaxed">
        The transcript with every tool call shown inline exactly where it fired, and an outcome panel carrying the machine-readable result. The tool calls are the visual proof of the grounding requirement above.
      </div>
    </div>
  );
};

export default ConversationDetail;
