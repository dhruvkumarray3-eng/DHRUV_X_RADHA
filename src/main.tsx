import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { AnimatePresence, motion } from "framer-motion";
import { BrainCircuit, ChevronLeft, ChevronRight, CircleStop, Flame, Heart, Mic2, Pause, Play, Repeat2, SkipBack, SkipForward, Sparkles, Users, Volume2, Zap } from "lucide-react";
import "./styles.css";

const BASE = import.meta.env.BASE_URL;
const scenes = [
  { kicker:"THE BOT THAT RUNS THE ROOM", title:"NOBITA X PRIME", sub:"Music. AI. Absolute control.", tone:"hero" },
  { kicker:"YOUR ENTIRE SOUNDTRACK", title:"PLAY ANYTHING.", sub:"YouTube · Spotify · Apple Music · SoundCloud — directly in Telegram voice chat.", tone:"music" },
  { kicker:"CONTROL THE ENERGY", title:"NO DEAD AIR.", sub:"Back. Pause. Resume. Skip. Stop. Seek.", tone:"controls" },
  { kicker:"THE QUEUE THAT THINKS AHEAD", title:"AUTOPLAY + LOOP", sub:"Related tracks keep the room moving. Loop the one that hits.", tone:"queue" },
  { kicker:"MEET YOUR GROUP'S SECOND BRAIN", title:"GROQ AI / LLAMA 3.3 70B", sub:"Auto-replies in any language. Learns the people behind the usernames.", tone:"ai" },
  { kicker:"BUILT FOR ADMINS", title:"POWER, WITHOUT THE NOISE.", sub:"Moderate. TagAll. Welcome. Nightmode. Notes. Filters.", tone:"admin" },
  { kicker:"EVERYTHING ELSE, TOO", title:"PLAY · CONNECT · PROTECT", sub:"Couples of the Day. Fun games. VC Logger. 24/7 keep-alive.", tone:"final" },
];

const featureGroups = [
  { label:"VOICE CHAT", items:["YouTube / Spotify / Apple Music / SoundCloud","Back · Pause · Resume · Skip · Stop","Seek to any timestamp","Autoplay related tracks","Loop current track"] },
  { label:"INTELLIGENCE", items:["Groq AI ChatBot · LLaMA 3.3 70B","Smart User Profiles for AI memory","Keyword Learning: custom replies"] },
  { label:"GROUP CONTROL", items:["Ban · Mute · Kick · Warn · Promote","TagAll every member","Welcome messages","Nightmode auto-lock"] },
  { label:"UTILITY", items:["Couple of the Day + fun games","Notes & Filters system","VC Logger","24/7 keep-alive · /ping"] },
];

function Wordmark({ small=false }: {small?:boolean}) {
  return <div className={small ? "wordmark small" : "wordmark"}><span>NOBITA X</span><b>PRIME</b><i>❤️‍🔥</i></div>;
}

function App() {
  const [scene, setScene] = useState(0);
  useEffect(() => {
    const id = window.setInterval(() => setScene(s => (s + 1) % scenes.length), 7200);
    return () => window.clearInterval(id);
  }, []);
  const current = scenes[scene];
  return <main className="video">
    <div className="noise" />
    <motion.div className="aurora aurora-a" animate={{ x: scene % 2 ? "10vw" : "-5vw", y: scene * -1.5 + "vh", scale: 1 + scene * .04 }} />
    <motion.div className="aurora aurora-b" animate={{ x: scene % 2 ? "-8vw" : "12vw", y: scene * 1.5 + "vh", rotate: scene * 14 }} />
    <div className="grid" />
    <motion.div className="persistent-ring" animate={{ rotate: scene * 42, scale: scene === 0 ? 1.35 : .82, x: scene === 0 ? "29vw" : "68vw", y: scene === 0 ? "25vh" : "56vh" }} />
    <header><Wordmark small /><div className="live"><span /> TELEGRAM POWER, REIMAGINED</div><div className="counter">0{scene+1} <em>/ 07</em></div></header>
    <AnimatePresence mode="sync">
      <motion.section key={scene} className={`scene ${current.tone}`} initial={{ clipPath:"polygon(0 0, 100% 0, 100% 0, 0 0)", opacity:0 }} animate={{ clipPath:"polygon(0 0, 100% 0, 100% 100%, 0 100%)", opacity:1 }} exit={{ clipPath:"polygon(0 100%, 100% 100%, 100% 100%, 0 100%)", opacity:0 }} transition={{ duration:.85, ease:[.7,0,.2,1] }}>
        <div className="scene-copy">
          <motion.div className="kicker" initial={{ x:-35, opacity:0 }} animate={{ x:0, opacity:1 }} transition={{ delay:.25, duration:.55 }}>{current.kicker}</motion.div>
          <motion.h1 initial={{ y:70, opacity:0, rotateX:35 }} animate={{ y:0, opacity:1, rotateX:0 }} transition={{ delay:.4, duration:.85, ease:[.16,1,.3,1] }}>{current.title}</motion.h1>
          <motion.p initial={{ y:25, opacity:0 }} animate={{ y:0, opacity:1 }} transition={{ delay:.85, duration:.6 }}>{current.sub}</motion.p>
        </div>
        <SceneArt scene={scene} />
      </motion.section>
    </AnimatePresence>
    <footer><div className="progress"><motion.div animate={{ width:`${((scene+1)/scenes.length)*100}%` }} transition={{ duration:.6 }} /></div><div className="footer-label">NOBITA X PRIME MUSIC BOT <span>•</span> @NOBITAXPRIME</div><div className="controls"><button onClick={()=>setScene((scene+scenes.length-1)%scenes.length)}><ChevronLeft /></button><button onClick={()=>setScene((scene+1)%scenes.length)}><ChevronRight /></button></div></footer>
  </main>;
}

function SceneArt({scene}:{scene:number}) {
  if (scene===0) return <div className="art hero-art"><motion.div className="heart-core" animate={{ scale:[1,1.08,1], rotate:[-3,3,-3] }} transition={{ duration:2.8, repeat:Infinity }}><Heart fill="currentColor" /></motion.div><div className="eq"><i/><i/><i/><i/><i/><i/><i/><i/><i/></div><div className="orbit orbit-1" /><div className="orbit orbit-2" /></div>;
  if (scene===1) return <div className="art player-art"><div className="album"><img src={`${BASE}attached_assets/generated_images/nobita_neon_stage.png`} /><span>NOW PLAYING</span><strong>THE ROOM<br/>IS YOURS</strong></div><div className="source-stack"><span>YT</span><span>SP</span><span>AM</span><span>SC</span></div><div className="vinyl" /></div>;
  if (scene===2) return <div className="art controls-art"><div className="control-dial"><div className="dial-track" /><Volume2 /><b>02:41</b></div><div className="control-pills"><span><SkipBack /></span><span><Pause /></span><span className="active"><Play /></span><span><SkipForward /></span><span><CircleStop /></span></div><div className="seek-line"><i /></div></div>;
  if (scene===3) return <div className="art queue-art"><div className="queue-card"><div className="queue-top"><span>UP NEXT</span><Repeat2 /><Zap /></div>{["Midnight City","After Hours","Goosebumps"].map((x,i)=><div className="queue-row" key={x}><b>0{i+1}</b><span>{x}</span><em>{i===0?"PLAYING":"QUEUED"}</em></div>)}</div><div className="autoplay"><Sparkles /> AUTOPLAY ON</div></div>;
  if (scene===4) return <div className="art ai-art"><img src={`${BASE}attached_assets/generated_images/nobita_ai_orbit.png`} /><div className="chat-bubbles"><span>what's the vibe tonight?</span><b>Make it loud. 🔥</b><span>अब सही गाना चलाओ</span></div><div className="ai-tag"><BrainCircuit /> GROQ AI <small>70B</small></div></div>;
  if (scene===5) return <div className="art admin-art">{featureGroups.slice(1,3).map((g,i)=><div className="admin-card" key={g.label}><span>{i===0?<Users />:<Sparkles />}</span><b>{g.label}</b>{g.items.slice(0,3).map(x=><small key={x}>✓ {x}</small>)}</div>)}</div>;
  return <div className="art final-art"><div className="feature-cloud">{["/ping","TAGALL","NIGHTMODE","VC LOGGER","NOTES","GAMES"].map((x,i)=><span key={x} style={{"--i":i} as React.CSSProperties}>{x}</span>)}</div><Flame className="final-flame" fill="currentColor" /></div>;
}

createRoot(document.getElementById("root")!).render(<App />);