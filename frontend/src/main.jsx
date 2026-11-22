import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

function App() {
  const [title, setTitle] = useState("Python API optimization");
  const [description, setDescription] = useState("Improve FastAPI endpoints and optimize PostgreSQL database queries.");
  const [results, setResults] = useState([]);
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);

  async function findExperts(e) {
    e.preventDefault(); setBusy(true); setNotice(""); setResults([]);
    try {
      const res = await fetch("http://127.0.0.1:8000/matches", {
        method: "POST", headers: {"Content-Type":"application/json"},
        body: JSON.stringify({title, description})
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail?.[0]?.msg || "Request failed");
      setResults(data.results); setNotice(data.decision_notice);
    } catch (err) { setNotice("Could not connect to the API. Start the backend first. " + err.message); }
    finally { setBusy(false); }
  }

  return <main className="shell">
    <header><div className="mark">H</div><div><h1>Human API</h1><p>Organizational expertise discovery</p></div></header>
    <section className="intro"><h2>Find the right expertise for the problem.</h2><p>Describe the work. Review suggested employees and the evidence behind each recommendation.</p></section>
    <form onSubmit={findExperts} className="panel">
      <label>Task title<input value={title} onChange={e=>setTitle(e.target.value)} required minLength="2"/></label>
      <label>Describe the problem<textarea rows="5" value={description} onChange={e=>setDescription(e.target.value)} required minLength="10"/></label>
      <button disabled={busy}>{busy ? "Matching…" : "Find experts"}</button>
    </form>
    {notice && <p className="notice">{notice}</p>}
    {results.length > 0 && <section><h2>Ranked candidates</h2><div className="results">
      {results.map((r,i)=><article className="candidate" key={r.employee_id}>
        <div className="candidateTop"><span className="rank">#{i+1}</span><div><h3>{r.name}</h3><small>{r.department} · {r.employee_id}</small></div><strong>{r.score}%</strong></div>
        <p><b>Evidence level:</b> {r.evidence_level}</p>
        <p><b>Matched terms:</b> {r.matched_terms.join(", ") || "No direct keyword overlap"}</p>
        <p>{r.explanation}</p>
      </article>)}
    </div></section>}
    <footer>Learning prototype · Keyword matching only · Human review required</footer>
  </main>;
}
createRoot(document.getElementById("root")).render(<App />);\n