import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Video,
} from "remotion";
import {LINES, OVERVIEW_BARS, SCENES, SUMMARY_ROWS} from "./timeline";

const CREAM = "#F6EEDC";
const CARD = "#FFFDF6";
const INK = "#2B2B26";
const MUTED = "#8A7D5F";
const RED = "#C0392B";
const YELLOW = "#FFD93D";
const YELLOW_TEXT = "#E8A100";
const BLUE = "#2E5E8C";
const CYAN = "#58C4DD";
const TRACK = "#EFE6CC";
const FONT = "'Noto Sans CJK SC', 'Noto Sans CJK', sans-serif";

type Clip = {file: string; from: number; to: number};
type Card = {
  index: string;
  name: string;
  en: string;
  price: string;
  priceSub: string;
  bullets: string[];
  verdict: string;
  chip: string;
  clip: Clip;
};
type Scene = {
  id: string;
  kind: string;
  title: string;
  num: number;
  start: number;
  end: number;
  card?: Card;
};

const scenes = SCENES as unknown as Scene[];
const lines = LINES as unknown as {
  id: string;
  text: string;
  scene: string;
  start: number;
  end: number;
}[];

const Seal: React.FC<{text: string; size?: number; style?: React.CSSProperties}> = ({
  text,
  size = 56,
  style,
}) => (
  <div
    style={{
      border: `${Math.max(4, size / 11)}px solid ${RED}`,
      borderRadius: 12,
      color: RED,
      fontFamily: FONT,
      fontSize: size,
      fontWeight: 900,
      padding: `${size * 0.12}px ${size * 0.36}px`,
      transform: "rotate(-5deg)",
      backgroundColor: "rgba(255,253,246,0.85)",
      display: "inline-block",
      lineHeight: 1.1,
      ...style,
    }}
  >
    {text}
  </div>
);

const Subtitle: React.FC<{text: string}> = ({text}) => (
  <div
    style={{
      position: "absolute",
      left: 0,
      right: 0,
      bottom: 54,
      display: "flex",
      justifyContent: "center",
      pointerEvents: "none",
    }}
  >
    <div
      style={{
        fontFamily: FONT,
        fontSize: 48,
        fontWeight: 900,
        color: "#fff",
        letterSpacing: 2,
        textShadow:
          "0 3px 0 #000, 3px 0 0 #000, -3px 0 0 #000, 0 -3px 0 #000, 3px 3px 0 #000, -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 0 6px 12px rgba(0,0,0,0.45)",
      }}
    >
      {text}
    </div>
  </div>
);

const TopBar: React.FC<{scene: Scene}> = ({scene}) => (
  <div
    style={{
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      height: 96,
      display: "flex",
      alignItems: "center",
      paddingLeft: 64,
      paddingRight: 64,
    }}
  >
    <div
      style={{
        backgroundColor: CYAN,
        color: "#0A0A0F",
        fontFamily: FONT,
        fontSize: 30,
        fontWeight: 900,
        borderRadius: 999,
        padding: "8px 26px",
      }}
    >
      AI · 上车合集
    </div>
    <div
      style={{
        fontFamily: FONT,
        fontSize: 40,
        fontWeight: 900,
        color: INK,
        marginLeft: 28,
      }}
    >
      Codex 全渠道合集
    </div>
    <div style={{flex: 1}} />
    <div style={{fontFamily: FONT, fontSize: 30, fontWeight: 700, color: MUTED}}>
      {scene.num} / {scenes.length}
    </div>
  </div>
);

const ChannelScene: React.FC<{scene: Scene; local: number}> = ({scene, local}) => {
  const {fps} = useVideoConfig();
  const card = scene.card as Card;
  const enter = spring({frame: local, fps, config: {damping: 100, stiffness: 160, mass: 0.6}});
  const sealPop = spring({
    frame: Math.max(0, local - 28),
    fps,
    config: {damping: 9, stiffness: 180, mass: 0.6},
  });
  return (
    <div
      style={{
        position: "absolute",
        left: 80,
        top: 128,
        width: 1760,
        height: 752,
        backgroundColor: CARD,
        borderRadius: 28,
        boxShadow: "0 18px 48px rgba(60,45,10,0.16)",
        opacity: enter,
        transform: `translateY(${interpolate(enter, [0, 1], [44, 0])}px)`,
      }}
    >
      {/* left column */}
      <div style={{position: "absolute", left: 64, top: 44, width: 830}}>
        <div style={{fontFamily: FONT, fontSize: 52, fontWeight: 900, color: INK}}>
          {card.index} · {card.name}
        </div>
        <div style={{display: "flex", alignItems: "baseline", marginTop: 18}}>
          <span style={{fontFamily: FONT, fontSize: 118, fontWeight: 900, color: BLUE, lineHeight: 1}}>
            {card.price}
          </span>
          <span style={{fontFamily: FONT, fontSize: 40, fontWeight: 700, color: MUTED, marginLeft: 22}}>
            {card.priceSub}
          </span>
        </div>
        <div style={{height: 2, backgroundColor: TRACK, marginTop: 30, marginBottom: 28}} />
        {card.bullets.map((b) => (
          <div
            key={b}
            style={{
              fontFamily: FONT,
              fontSize: 37,
              fontWeight: 700,
              color: INK,
              lineHeight: 1.35,
              marginBottom: 16,
              display: "flex",
            }}
          >
            <span style={{color: YELLOW_TEXT, marginRight: 14}}>▸</span>
            <span>{b}</span>
          </div>
        ))}
        <div style={{fontFamily: FONT, fontSize: 28, color: MUTED, marginTop: 26}}>
          大陆：直连用不了 · 订阅境外支付
        </div>
      </div>

      {/* verdict seal next to price */}
      <div
        style={{
          position: "absolute",
          left: 690,
          top: 118,
          opacity: sealPop,
          transform: `rotate(-5deg) scale(${interpolate(sealPop, [0, 1], [1.7, 1])})`,
        }}
      >
        <Seal text={card.verdict} size={54} />
      </div>

      {/* right: real footage window */}
      <div style={{position: "absolute", left: 960, top: 60, width: 760}}>
        <div
          style={{
            width: 760,
            height: 428,
            borderRadius: 18,
            overflow: "hidden",
            border: `3px solid #E8DFC8`,
            backgroundColor: "#111",
          }}
        >
          <Video
            src={staticFile(card.clip.file)}
            startFrom={Math.round(card.clip.from * 30)}
            endAt={Math.round(card.clip.to * 30)}
            loop
            muted
            style={{width: "100%", height: "100%", objectFit: "cover"}}
          />
        </div>
        <div
          style={{
            fontFamily: FONT,
            fontSize: 26,
            color: MUTED,
            textAlign: "center",
            marginTop: 14,
          }}
        >
          真实画面 · OpenAI 官方演示
        </div>
        <div
          style={{
            marginTop: 26,
            backgroundColor: "#FFF6D6",
            border: `2px solid ${YELLOW}`,
            borderRadius: 14,
            padding: "16px 22px",
            fontFamily: FONT,
            fontSize: 32,
            fontWeight: 900,
            color: INK,
            textAlign: "center",
          }}
        >
          {card.chip}
        </div>
      </div>
    </div>
  );
};

const OverviewScene: React.FC<{local: number}> = ({local}) => {
  const {fps} = useVideoConfig();
  const enter = spring({frame: local, fps, config: {damping: 100, stiffness: 160, mass: 0.6}});
  const trackW = 1180;
  return (
    <div
      style={{
        position: "absolute",
        left: 80,
        top: 128,
        width: 1760,
        height: 752,
        backgroundColor: CARD,
        borderRadius: 28,
        boxShadow: "0 18px 48px rgba(60,45,10,0.16)",
        opacity: enter,
        transform: `translateY(${interpolate(enter, [0, 1], [44, 0])}px)`,
      }}
    >
      <div style={{fontFamily: FONT, fontSize: 58, fontWeight: 900, color: INK, marginLeft: 64, marginTop: 40}}>
        五个渠道，价格全在这
      </div>
      <div style={{marginLeft: 64, marginTop: 36}}>
        {(OVERVIEW_BARS as {label: string; price: string; value: number; highlight: boolean}[]).map(
          (bar, i) => {
            const grow = interpolate(local - 15 - i * 5, [0, 28], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            const w = Math.max(bar.value === 0 ? 0 : 14, (bar.value / 500) * trackW * grow);
            return (
              <div key={bar.label} style={{display: "flex", alignItems: "center", height: 96}}>
                <div style={{width: 170, fontFamily: FONT, fontSize: 42, fontWeight: 900, color: INK}}>
                  {bar.label}
                </div>
                <div
                  style={{
                    width: trackW,
                    height: 54,
                    backgroundColor: TRACK,
                    borderRadius: 27,
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      width: w,
                      height: "100%",
                      backgroundColor: bar.highlight ? YELLOW : BLUE,
                      borderRadius: 27,
                    }}
                  />
                </div>
                <div style={{fontFamily: FONT, fontSize: 44, fontWeight: 900, color: INK, marginLeft: 24}}>
                  {bar.price}
                </div>
                {bar.highlight && (
                  <div style={{marginLeft: 22}}>
                    <Seal text="最值" size={34} />
                  </div>
                )}
              </div>
            );
          },
        )}
      </div>
      <div style={{fontFamily: FONT, fontSize: 28, color: MUTED, marginLeft: 64, marginTop: 26}}>
        价格为美元原价，不含税 · 人民币按 1 美元 ≈ 6.66 元折算
      </div>
    </div>
  );
};

const HookScene: React.FC<{local: number}> = ({local}) => {
  const {fps} = useVideoConfig();
  const t1 = spring({frame: local, fps, config: {damping: 100, stiffness: 140, mass: 0.6}});
  const t2 = spring({frame: Math.max(0, local - 12), fps, config: {damping: 100, stiffness: 140, mass: 0.6}});
  const chips = ["免费 $0", "Go $8", "Plus $20", "Pro $100起", "API 按量"];
  return (
    <div style={{position: "absolute", left: 0, right: 0, top: 0, bottom: 0, textAlign: "center"}}>
      <div style={{fontFamily: FONT, fontSize: 46, color: MUTED, marginTop: 196, opacity: t1}}>
        OpenAI 的编程助手
      </div>
      <div
        style={{
          fontFamily: FONT,
          fontSize: 148,
          fontWeight: 900,
          color: INK,
          lineHeight: 1.15,
          marginTop: 18,
          opacity: t1,
          transform: `translateY(${interpolate(t1, [0, 1], [40, 0])}px)`,
        }}
      >
        Codex 上车
      </div>
      <div
        style={{
          fontFamily: FONT,
          fontSize: 148,
          fontWeight: 900,
          color: YELLOW_TEXT,
          lineHeight: 1.15,
          opacity: t2,
          transform: `translateY(${interpolate(t2, [0, 1], [40, 0])}px)`,
        }}
      >
        0 元就能用
      </div>
      <div style={{fontFamily: FONT, fontSize: 54, color: INK, marginTop: 36, opacity: t2}}>
        五个渠道，一次讲清楚
      </div>
      <div style={{display: "flex", justifyContent: "center", gap: 26, marginTop: 56, opacity: t2}}>
        {chips.map((c) => (
          <div
            key={c}
            style={{
              backgroundColor: CARD,
              border: `2px solid #E8DFC8`,
              borderRadius: 16,
              padding: "18px 30px",
              fontFamily: FONT,
              fontSize: 40,
              fontWeight: 900,
              color: INK,
              boxShadow: "0 8px 22px rgba(60,45,10,0.12)",
            }}
          >
            {c}
          </div>
        ))}
      </div>
    </div>
  );
};

const SummaryScene: React.FC<{local: number}> = ({local}) => {
  const {fps} = useVideoConfig();
  const enter = spring({frame: local, fps, config: {damping: 100, stiffness: 160, mass: 0.6}});
  const rows = SUMMARY_ROWS as {name: string; price: string; one: string; verdict: string}[];
  return (
    <div
      style={{
        position: "absolute",
        left: 80,
        top: 128,
        width: 1760,
        height: 752,
        backgroundColor: CARD,
        borderRadius: 28,
        boxShadow: "0 18px 48px rgba(60,45,10,0.16)",
        opacity: enter,
        transform: `translateY(${interpolate(enter, [0, 1], [44, 0])}px)`,
      }}
    >
      <div style={{fontFamily: FONT, fontSize: 58, fontWeight: 900, color: INK, marginLeft: 64, marginTop: 36}}>
        汇总：普通人怎么选
      </div>
      <div style={{marginLeft: 64, marginRight: 64, marginTop: 24}}>
        {rows.map((r, i) => (
          <div
            key={r.name}
            style={{
              display: "flex",
              alignItems: "center",
              height: 88,
              backgroundColor: r.name === "Plus" ? "#FFF6D6" : "transparent",
              borderRadius: 14,
              borderBottom: i < rows.length - 1 ? `2px solid ${TRACK}` : "none",
              paddingLeft: 20,
              paddingRight: 20,
            }}
          >
            <div style={{width: 250, fontFamily: FONT, fontSize: 44, fontWeight: 900, color: INK}}>{r.name}</div>
            <div style={{width: 320, fontFamily: FONT, fontSize: 44, fontWeight: 900, color: BLUE}}>{r.price}</div>
            <div style={{flex: 1, fontFamily: FONT, fontSize: 40, fontWeight: 700, color: INK}}>{r.one}</div>
            <Seal text={r.verdict} size={36} />
          </div>
        ))}
      </div>
      <div
        style={{
          fontFamily: FONT,
          fontSize: 30,
          color: MUTED,
          textAlign: "center",
          marginTop: 22,
        }}
      >
        数据：OpenAI 官网定价页，2026 年 11 月 · 画面：OpenAI 官方演示
      </div>
    </div>
  );
};

export const CodexLong: React.FC = () => {
  const frame = useCurrentFrame();
  const scene = scenes.find((s) => frame >= s.start && frame < s.end) ?? scenes[scenes.length - 1];
  const local = frame - scene.start;
  const active = [...lines]
    .reverse()
    .find((l) => frame >= l.start && frame < l.end + 12);

  return (
    <AbsoluteFill style={{backgroundColor: CREAM, fontFamily: FONT}}>
      {/* soft decor circles */}
      <div
        style={{
          position: "absolute",
          width: 520,
          height: 520,
          borderRadius: "50%",
          backgroundColor: "#FFF8E6",
          top: -180,
          right: -120,
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 420,
          height: 420,
          borderRadius: "50%",
          backgroundColor: "#F3E9CE",
          bottom: -160,
          left: -140,
        }}
      />
      <TopBar scene={scene} />
      {scene.kind === "hook" && <HookScene local={local} />}
      {scene.kind === "overview" && <OverviewScene local={local} />}
      {(scene.kind === "free" ||
        scene.kind === "go" ||
        scene.kind === "plus" ||
        scene.kind === "pro" ||
        scene.kind === "api") && <ChannelScene scene={scene} local={local} />}
      {scene.kind === "summary" && <SummaryScene local={local} />}
      {active && <Subtitle text={active.text} />}
    </AbsoluteFill>
  );
};
