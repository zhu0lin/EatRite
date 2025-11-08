import React, { useEffect, useRef } from "react";
import { Animated, Dimensions, StyleSheet } from "react-native";

const { width, height } = Dimensions.get("window");

const EMOJIS = [
  "🍎",
  "🥦",
  "🥕",
  "🍞",
  "🍚",
  "🥩",
  "🍗",
  "🥚",
  "🧀",
  "🍤",
  "🥑",
  "🍅",
  "🌽",
  "🥔",
  "🥬",
  "🍌",
  "🍓",
  "🍣",
  "🥖",
  "🥜",
];

export default function FloatingShapes() {
  return (
    <>
      {EMOJIS.map((emoji, i) => (
        <FloatingEmoji
          key={i}
          emoji={emoji}
          delay={i * 1000 + Math.random() * 1500}
        />
      ))}
    </>
  );
}

function FloatingEmoji({ emoji, delay }: { emoji: string; delay: number }) {
  const translateY = useRef(new Animated.Value(height)).current;
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const loopAnimation = () => {
      Animated.sequence([
        Animated.delay(delay),
        Animated.parallel([
          Animated.timing(translateY, {
            toValue: -120,
            duration: 12000 + Math.random() * 3000,
            useNativeDriver: true,
          }),
          Animated.sequence([
            Animated.timing(opacity, {
              toValue: 0.35, // more visible mid-animation
              duration: 2500,
              useNativeDriver: true,
            }),
            Animated.timing(opacity, {
              toValue: 0,
              duration: 2500,
              delay: 6000,
              useNativeDriver: true,
            }),
          ]),
        ]),
      ]).start(() => {
        translateY.setValue(height + Math.random() * 50);
        opacity.setValue(0);
        loopAnimation();
      });
    };

    loopAnimation();
  }, []);

  const translateX = Math.random() * (width - 40);
  const scale = 0.8 + Math.random() * 0.4;
  const rotation = Math.random() * 20 - 10;

  return (
    <Animated.Text
      style={[
        styles.emoji,
        {
          opacity,
          transform: [
            { translateY },
            { translateX },
            { scale },
            { rotate: `${rotation}deg` },
          ],
        },
      ]}
    >
      {emoji}
    </Animated.Text>
  );
}

const styles = StyleSheet.create({
  emoji: {
    position: "absolute",
    fontSize: 38,
    opacity: 0.6, // 👈 default lower opacity too
  },
});
