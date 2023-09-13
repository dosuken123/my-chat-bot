import { ChatWindow } from "../app/components/ChatWindow";
import { ToastContainer } from "react-toastify";

export default function Home() {
  return (
    <>
      <ToastContainer />
      <ChatWindow
        apiBaseUrl={process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8080"}
        titleText="Street Fighter 6 AI"
        placeholder="What is startup frame of Luke's standing light punch?"
      ></ChatWindow>
    </>
  );
}
