"use client";
import "../styles/globals.css";
import { ReactNode } from "react";
import Header from "./header";
import Sidebar from "./sidebar";
import Footer from "./footer";

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <html lang="es">
      <body><div className="min-h-screen flex flex-col">
      <Header />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 overflow-y-auto">{children}</main>
      </div>
      <Footer />
    </div></body>
    </html>
  );
}
