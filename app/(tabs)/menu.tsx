import { LinearGradient } from "expo-linear-gradient";
import { useRouter } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useEffect, useRef } from "react";
import {
  Animated,
  Dimensions,
  Easing,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const { height } = Dimensions.get("window");

export default function Menu() {
  const router = useRouter();
  const slideAnim = useRef(new Animated.Value(-height)).current; // start off-screen

  useEffect(() => {
    Animated.timing(slideAnim, {
      toValue: 0,
      duration: 350,
      easing: Easing.out(Easing.ease),
      useNativeDriver: true,
    }).start();
  }, []);

  const handleNavigate = (path: string) => {
    router.push(path);
  };

  const handleLogout = () => {
    console.log("Logging out...");
    router.replace("./index"); // back to login
  };

  return (
    <View style={styles.root}>
      {/* 🖤 Keep safe areas black */}
      <SafeAreaView edges={["top", "bottom"]} style={styles.safeArea}>
        {/* 🌈 Background gradient */}
        <LinearGradient
          colors={["rgba(250, 255, 230, 0.95)", "rgba(220, 255, 230, 0.95)"]}
          start={{ x: 0.5, y: 0 }}
          end={{ x: 0.5, y: 1 }}
          style={StyleSheet.absoluteFill}
        />

        {/* 📜 Dropdown Menu */}
        <Animated.View
          style={[
            styles.dropdownContainer,
            { transform: [{ translateY: slideAnim }] },
          ]}
        >
          <TouchableOpacity
            style={styles.menuItem}
            onPress={() => handleNavigate("./settings")}
          >
            <Text style={styles.menuText}>⚙️ Settings</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.menuItem}
            onPress={() => handleNavigate("./allergies")}
          >
            <Text style={styles.menuText}>🚫 Allergies</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.menuItem}
            onPress={() => handleNavigate("./scanner")}
          >
            <Text style={styles.menuText}>📷 Scanner</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.menuItem}
            onPress={() => handleNavigate("./about")}
          >
            <Text style={styles.menuText}>ℹ️ About</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.menuItem, styles.logout]}
            onPress={handleLogout}
          >
            <Text style={[styles.menuText, { color: "#fff" }]}>🚪 Log Out</Text>
          </TouchableOpacity>
        </Animated.View>
      </SafeAreaView>

      {/* 🖤 White icons on black background */}
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
  dropdownContainer: {
    marginTop: 80,
    marginHorizontal: 30,
    borderRadius: 16,
    backgroundColor: "rgba(255,255,255,0.9)",
    paddingVertical: 15,
    shadowColor: "#000",
    shadowOpacity: 0.15,
    shadowOffset: { width: 0, height: 3 },
    shadowRadius: 6,
  },
  menuItem: {
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: "#ddd",
  },
  menuText: {
    fontSize: 18,
    fontWeight: "600",
    color: "#333",
  },
  logout: {
    backgroundColor: "#ff6b6b",
    borderBottomWidth: 0,
    borderRadius: 12,
    margin: 10,
  },
});
