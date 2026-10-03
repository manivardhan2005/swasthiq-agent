import React from 'react';
import { Link } from 'react-router-dom';

const HandoffQueue = () => {
  return (
    <div className="max-w-[1000px] mx-auto">
      {/* Header section inside a white card-like shape or just plain background? */}
      <div className="mb-6 flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-bold text-[#003C89] mb-1">1. Handoff Queue</h1>
          <p className="text-sm text-[#475467]">Sunrise Clinic, Dehradun — conversations the agent escalated</p>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-[#E4E7EC] shadow-sm mb-8 overflow-hidden">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-xl font-bold text-[#101828]">Handoff Queue</h2>
              <p className="text-sm text-[#475467] mt-1">Sunrise Clinic, Dehradun — conversations the agent escalated</p>
            </div>
            <button className="text-xs font-semibold text-blue-600 bg-blue-50 px-3 py-1.5 rounded-full">
              4 OPEN
            </button>
          </div>

          <div className="grid grid-cols-4 gap-4 mb-8">
            <div className="border border-[#E4E7EC] rounded-lg p-4">
              <div className="text-xs font-semibold text-[#475467] tracking-wider mb-2">CONVERSATIONS</div>
              <div className="text-2xl font-bold text-[#101828]">37</div>
              <div className="text-xs text-[#475467] mt-1">today</div>
            </div>
            <div className="border border-[#E4E7EC] rounded-lg p-4">
              <div className="text-xs font-semibold text-[#475467] tracking-wider mb-2">COMPLETED BY AGENT</div>
              <div className="text-2xl font-bold text-[#101828]">31</div>
              <div className="text-xs text-[#475467] mt-1">84%</div>
            </div>
            <div className="border border-[#E4E7EC] rounded-lg p-4">
              <div className="text-xs font-semibold text-[#475467] tracking-wider mb-2">ESCALATED</div>
              <div className="text-2xl font-bold text-[#101828]">6</div>
              <div className="text-xs text-blue-600 font-medium mt-1">4 still open</div>
            </div>
            <div className="border border-[#E4E7EC] rounded-lg p-4">
              <div className="text-xs font-semibold text-[#475467] tracking-wider mb-2">URGENT</div>
              <div className="text-2xl font-bold text-[#101828]">1</div>
              <div className="text-xs text-red-600 font-medium mt-1">clinical, unresolved</div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-bold text-[#101828] mb-4">Open handoffs</h3>
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[#E4E7EC] text-xs font-semibold text-[#475467] tracking-wider">
                  <th className="pb-3 font-semibold">CONVERSATION</th>
                  <th className="pb-3 font-semibold">CALLER SAID</th>
                  <th className="pb-3 font-semibold">REASON</th>
                  <th className="pb-3 font-semibold">TIME</th>
                  <th className="pb-3"></th>
                </tr>
              </thead>
              <tbody className="text-sm text-[#101828]">
                <tr className="border-b border-[#E4E7EC] hover:bg-gray-50">
                  <td className="py-4 font-medium"><Link to="/cv_4471" className="hover:underline">cv_4471</Link></td>
                  <td className="py-4">"Seene mein dard ho raha hai"</td>
                  <td className="py-4">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-red-50 text-red-700">
                      CLINICAL
                    </span>
                  </td>
                  <td className="py-4 text-[#475467]">11:42</td>
                  <td className="py-4 text-right">
                    <button className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold py-1.5 px-4 rounded border border-blue-700">Resolve</button>
                  </td>
                </tr>
                <tr className="border-b border-[#E4E7EC] hover:bg-gray-50">
                  <td className="py-4 font-medium">cv_4468</td>
                  <td className="py-4">Cancel for a different patient</td>
                  <td className="py-4">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-orange-50 text-orange-700">
                      NOT AUTHORISED
                    </span>
                  </td>
                  <td className="py-4 text-[#475467]">11:20</td>
                  <td className="py-4 text-right">
                    <button className="bg-white hover:bg-gray-50 text-[#475467] text-xs font-bold py-1.5 px-4 rounded border border-[#D0D5DD]">Resolve</button>
                  </td>
                </tr>
                <tr className="border-b border-[#E4E7EC] hover:bg-gray-50">
                  <td className="py-4 font-medium">cv_4463</td>
                  <td className="py-4">"Sharma ji ke liye" — 3 matches</td>
                  <td className="py-4">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-yellow-50 text-yellow-700">
                      AMBIGUOUS PATIENT
                    </span>
                  </td>
                  <td className="py-4 text-[#475467]">10:57</td>
                  <td className="py-4 text-right">
                    <button className="bg-white hover:bg-gray-50 text-[#475467] text-xs font-bold py-1.5 px-4 rounded border border-[#D0D5DD]">Resolve</button>
                  </td>
                </tr>
                <tr className="hover:bg-gray-50">
                  <td className="py-4 font-medium">cv_4455</td>
                  <td className="py-4">"Ye dawai lun ya nahi?"</td>
                  <td className="py-4">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-pink-50 text-pink-700">
                      MEDICAL ADVICE
                    </span>
                  </td>
                  <td className="py-4 text-[#475467]">10:18</td>
                  <td className="py-4 text-right">
                    <button className="bg-white hover:bg-gray-50 text-[#475467] text-xs font-bold py-1.5 px-4 rounded border border-[#D0D5DD]">Resolve</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <div className="text-center text-sm text-[#475467] italic mt-8 max-w-2xl mx-auto leading-relaxed">
        Counters across the top, then the open handoffs the agent escalated, each with what the caller said, the reason, and a way to resolve it.
      </div>
    </div>
  );
};

export default HandoffQueue;
