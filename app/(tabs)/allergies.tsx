import { LinearGradient } from "expo-linear-gradient";
import { useRouter } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import FloatingShapes from "../../components/FloatingShapes";

export default function Allergies() {
  const router = useRouter();
  const [selected, setSelected] = useState<string[]>([]);

  const handleSelect = (option: string) => {
    setSelected((prev) =>
      prev.includes(option)
        ? prev.filter((item) => item !== option)
        : [...prev, option]
    );
  };

  const handleContinue = () => {
    if (selected.length > 0) {
      console.log("Selected allergies:", selected);
      router.push("./scanner");
    } else {
      console.log("Please select at least one allergy");
    }
  };

  const options = [
    "Milk 🥛",
    "Eggs 🥚",
    "Fish 🐟",
    "Shellfish 🦐",
    "Tree Nuts 🌰",
    "Peanuts 🥜",
    "Wheat 🌾",
    "Soy 🌱",
    "Sesame 🌼",
  ];

  return (
    <View style={styles.root}>
      <SafeAreaView edges={["top", "bottom"]} style={styles.safeArea}>
        {/* 🌈 Gradient background (same as sign-in / preferences page) */}
        <LinearGradient
          colors={["rgba(250, 255, 230, 0.95)", "rgba(220, 255, 230, 0.95)"]}
          start={{ x: 0.5, y: 0 }}
          end={{ x: 0.5, y: 1 }}
          style={StyleSheet.absoluteFill}
        />

        <FloatingShapes />

        <KeyboardAvoidingView
          behavior={Platform.OS === "ios" ? "padding" : undefined}
          style={{ flex: 1 }}
        >
          <ScrollView contentContainerStyle={styles.container}>
            <Text style={styles.title}>
              <Text style={{ color: "#5ac18e" }}>EAT</Text>
              <Text style={{ color: "#222" }}>RITE</Text>
            </Text>

            <Text style={styles.subtitle}>Select your allergies</Text>

            <View style={styles.optionsContainer}>
              {options.map((option, i) => {
                const isSelected = selected.includes(option);
                return (
                  <TouchableOpacity
                    key={i}
                    style={[
                      styles.optionBtn,
                      isSelected && styles.optionBtnSelected,
                    ]}
                    activeOpacity={0.8}
                    onPress={() => handleSelect(option)}
                  >
                    <Text
                      style={[
                        styles.optionText,
                        isSelected && styles.optionTextSelected,
                      ]}
                    >
                      {option}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>

            <TouchableOpacity
              style={[
                styles.nextBtn,
                selected.length === 0 && { opacity: 0.5 },
              ]}
              onPress={handleContinue}
              disabled={selected.length === 0}
            >
              <Text style={styles.nextText}>Continue</Text>
            </TouchableOpacity>
          </ScrollView>
        </KeyboardAvoidingView>
      </SafeAreaView>

      <StatusBar style="light" backgroundColor="black" />
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: "black",
  },
  safeArea: {
    flex: 1,
    backgroundColor: "transparent",
  },
  container: {
    paddingVertical: 60,
    paddingHorizontal: 25,
    alignItems: "center",
  },
  title: {
    fontSize: 40,
    fontWeight: "800",
    color: "#222",
    letterSpacing: 1.5,
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: "#444",
    marginBottom: 30,
    fontWeight: "500",
  },
  optionsContainer: {
    width: "100%",
    marginBottom: 30,
  },
  optionBtn: {
    backgroundColor: "rgba(255, 255, 255, 0.85)",
    borderRadius: 14,
    paddingVertical: 14,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "#ddd",
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.08,
    shadowOffset: { width: 0, height: 3 },
    shadowRadius: 5,
  },
  optionBtnSelected: {
    backgroundColor: "rgba(90, 193, 142, 0.3)",
    borderColor: "#5ac18e",
  },
  optionText: {
    fontSize: 17,
    fontWeight: "600",
    color: "#333",
  },
  optionTextSelected: {
    color: "#2c7a59",
  },
  nextBtn: {
    backgroundColor: "#5ac18e",
    borderRadius: 14,
    paddingVertical: 15,
    paddingHorizontal: 50,
    shadowColor: "#000",
    shadowOpacity: 0.15,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 5,
  },
  nextText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "700",
    letterSpacing: 0.5,
  },
});
