"use client";
import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-white shadow py-4 px-6 flex items-center justify-between">
      <h1 className="text-xl font-bold">Operador SDLX - Consola</h1>
      <nav>
        <Link href="#">
          <span className="text-gray-600 hover:text-gray-900 px-3">Inicio</span>
        </Link>
        <Link href="#">
          <span className="text-gray-600 hover:text-gray-900 px-3">Perfil</span>
        </Link>
      </nav>
    </header>
  );
}
