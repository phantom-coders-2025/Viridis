import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col w-full">
        <TopBar />
        <main className="flex-1 p-6 overflow-auto">
          <Outlet /> {/* Nested routes render here */}
        </main>
      </div>
    </div>
  );
};

export default Layout;
