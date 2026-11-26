import {Composition} from "remotion";
import {CodexLong} from "./CodexLong";
import {TOTAL_FRAMES} from "./timeline";

export const MyComposition = () => {
  return (
    <Composition
      id="CodexLong"
      component={CodexLong}
      durationInFrames={TOTAL_FRAMES}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
