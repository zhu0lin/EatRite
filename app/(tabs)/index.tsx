import { LinearGradient } from "expo-linear-gradient";
import { useRouter } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import FloatingShapes from "../../components/FloatingShapes";

export default function Index() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignIn = () => {
    console.log("Sign in:", { email, password });
    router.push("./preferences");
  };

  const handleSocialLogin = (provider: string) => {
    console.log(`Logging in with ${provider}`);
  };

  return (
    // 👇 This outer View guarantees black even behind system gestures
    <View style={{ flex: 1, backgroundColor: "black" }}>
      {/* 🖤 SafeAreaView sits above, transparent so black shows */}
      <SafeAreaView
        edges={["top", "bottom"]}
        style={{ flex: 1, backgroundColor: "transparent" }}
      >
        {/* 🌈 Gradient */}
        <LinearGradient
          colors={[
            "rgba(250, 255, 230, 0.95)", // soft yellow-green top
            "rgba(220, 255, 230, 0.95)", // minty bottom
          ]}
          start={{ x: 0.5, y: 0 }}
          end={{ x: 0.5, y: 1 }}
          style={StyleSheet.absoluteFill}
        />

        {/* 🍎 Floating emojis */}
        <FloatingShapes />

        {/* 🧍 Main sign-in content */}
        <KeyboardAvoidingView
          style={styles.overlay}
          behavior={Platform.OS === "ios" ? "padding" : undefined}
        >
          <Text style={styles.title}>
            <Text style={{ color: "#5ac18e" }}>EAT</Text>
            <Text style={{ color: "#222" }}>RITE</Text>
          </Text>

          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Email"
              placeholderTextColor="#888"
              keyboardType="email-address"
              autoCapitalize="none"
              value={email}
              onChangeText={setEmail}
            />

            <TextInput
              style={styles.input}
              placeholder="Password"
              placeholderTextColor="#888"
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />
          </View>

          <TouchableOpacity style={styles.signInBtn} onPress={handleSignIn}>
            <Text style={styles.signInText}>Sign In</Text>
          </TouchableOpacity>

          <View style={styles.divider}>
            <View style={styles.line} />
            <Text style={styles.orText}>OR</Text>
            <View style={styles.line} />
          </View>

          <View style={styles.socialContainer}>
            <TouchableOpacity
              style={[styles.socialBtn, { backgroundColor: "#DB4437" }]}
              onPress={() => handleSocialLogin("Google")}
            >
              <Text style={styles.socialText}>Continue with Google</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.socialBtn, { backgroundColor: "#000" }]}
              onPress={() => handleSocialLogin("Apple")}
            >
              <Text style={[styles.socialText, { color: "#fff" }]}>
                Continue with Apple
              </Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            onPress={() => console.log("Forgot password")}
            style={{ marginTop: 25 }}
          >
            <Text style={styles.forgotText}>Forgot Password?</Text>
          </TouchableOpacity>
        </KeyboardAvoidingView>
      </SafeAreaView>

      {/* 🖤 Status bar (white icons, solid black background) */}
      <StatusBar style="light" backgroundColor="black" translucent={false} />
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 30,
    paddingBottom: 60,
  },
  title: {
    fontSize: 46,
    fontWeight: "800",
    color: "#222",
    letterSpacing: 2,
    marginBottom: 40,
    textShadowColor: "rgba(0,0,0,0.1)",
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  inputContainer: {
    width: "100%",
    marginBottom: 20,
  },
  input: {
    width: "100%",
    backgroundColor: "#fff",
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "#ddd",
    padding: 14,
    fontSize: 16,
    marginBottom: 15,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 4,
  },
  signInBtn: {
    width: "100%",
    backgroundColor: "#7adbb6",
    borderRadius: 14,
    paddingVertical: 15,
    marginTop: 10,
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 5,
  },
  signInText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "700",
    textAlign: "center",
    letterSpacing: 0.5,
  },
  divider: {
    flexDirection: "row",
    alignItems: "center",
    width: "100%",
    marginVertical: 25,
  },
  line: {
    flex: 1,
    height: 1,
    backgroundColor: "#bbb",
  },
  orText: {
    marginHorizontal: 10,
    color: "#666",
    fontWeight: "600",
  },
  socialContainer: {
    width: "100%",
  },
  socialBtn: {
    paddingVertical: 14,
    borderRadius: 12,
    marginBottom: 12,
  },
  socialText: {
    color: "#fff",
    textAlign: "center",
    fontWeight: "600",
    letterSpacing: 0.5,
  },
  forgotText: {
    color: "#444",
    fontSize: 15,
    textDecorationLine: "underline",
  },
});
