"use client";

import { useLogin } from "@/app/hooks/useLogin";

const LoginButton = () => {
  const { mutate: login, isPending } = useLogin();

  return (
    <button
      onClick={() => login()}
      disabled={isPending}
      className={`px-12 py-4 text-white text-lg rounded-full transition-colors font-medium ${
        isPending
          ? "bg-gray-600 cursor-not-allowed opacity-50"
          : "bg-gray-800 hover:bg-gray-700"
      }`}
    >
      {isPending ? "Signing in..." : "Sign In with Google"}
    </button>
  );
};
export default LoginButton;
