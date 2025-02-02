"use client";
import Link from "next/link";
import Image from "next/image";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-[#1a2433] text-white flex flex-col">
      <div className="p-6 bg-white">
        {/* Imagen de logo placeholder */}
        <Image
          src="https://via.placeholder.com/180x80?text=Logo"
          alt="Logo"
          width={180}
          height={80}
          className="object-contain"
          priority
        />
      </div>
      <nav className="flex-1 px-4">
        <div className="space-y-1">
          <Link href="#">
            <span className="block px-3 py-2 text-gray-300 hover:text-white rounded-lg">
              Dashboard
            </span>
          </Link>
          <Link href="#">
            <span className="block px-3 py-2 text-gray-300 hover:text-white rounded-lg">
              Mis Solicitudes
            </span>
          </Link>
          <Link href="#">
            <span className="block px-3 py-2 text-gray-300 hover:text-white rounded-lg">
              Documentación
            </span>
          </Link>
          <Link href="#">
            <span className="block px-3 py-2 text-gray-300 hover:text-white rounded-lg">
              Mi plan
            </span>
          </Link>
          <Link href="#">
            <span className="block px-3 py-2 bg-[#3498db] text-white rounded-lg">
              Operador SDLC
            </span>
          </Link>
        </div>
      </nav>
      <div className="p-4 text-xs text-gray-400">Deloitte TS Labs ©2025</div>
    </aside>
  );
}
