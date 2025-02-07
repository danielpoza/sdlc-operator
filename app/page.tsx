"use client";
import { useState, KeyboardEvent } from "react";
import Layout from "@/app/components/layout";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw"

const stages = [
  {
    title: "Definición de Requisitos",
    description: "Inspiración y definición para Product Owners",
  },
  {
    title: "Análisis y Diseño",
    description: "Asistencia a arquitectos en base a principios de la organización",
  },
  {
    title: "Desarrollo",
    description: "Automatización y ayuda al desarrollo de componentes y su despliegue",
  },
  {
    title: "Pruebas",
    description: "Estrategia QA, generación de datos y scripts de prueba",
  },
  {
    title: "Operación y Observabilidad",
    description: "Análisis de logs y alertas. Remedación 0-touch",
  },
];

export default function Home() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "**Hola**, ¿en qué puedo ayudarte hoy?\n\n- Punto 1\n- Punto 2" },
  ]);
  const [input, setInput] = useState("");
  const [selectedStage, setSelectedStage] = useState<number | null>(null);

  // Función que se llama cuando se selecciona una etapa
  const handleSelectStage = (index: number) => {
    setSelectedStage(index);
    // Aquí puedes agregar la lógica adicional, por ejemplo, almacenar la selección
    console.log("Etapa seleccionada:", stages[index].title);
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { sender: "user", text: input }]);
    try {
      const response = await fetch("http://127.0.0.1:8000/process_message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });
      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: data.message },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error al llamar al backend" },
      ]);
    }
    setInput("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Layout>
      <div className="flex flex-col gap-6 h-full" >
        {/* Sección superior: Título y botones */}
        <div style={{
              backgroundImage: "url('/background2.png')",
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}>
          <h2 className="text-lg font-semibold mb-4 text-center">
            Etapas del Ciclo de Vida de Desarrollo Software
          </h2>
          <div className="max-w-6xl mx-auto px-4">
            <div className="grid grid-cols-5 gap-4">
              {stages.map((stage, index) => (
                <button
                  key={index}
                  onClick={() => handleSelectStage(index)}
                  className={`w-56 h-48 bg-white border border-gray-300 rounded-xl flex flex-col items-center justify-center p-4 transition-shadow
                    ${selectedStage === index ? "ring-4 ring-blue-500" : "hover:shadow-xl"}`}
                >
                  <span className="font-bold text-base text-center">
                    {stage.title}
                  </span>
                  <span className="text-sm italic mt-2 text-gray-500 text-center">
                    {stage.description}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Línea divisoria */}
        <hr className="border-t border-gray-300 my-6" />

        {/* Sección inferior: Chat */}
        <div className="flex flex-col gap-4">
          <h2 className="text-3xl font-bold text-center text-gray-800">
            Asistente SDLC
          </h2>
          {/* Contenedor del chat con altura fija y scroll interno */}
          <div className="h-96 w-full max-w-3xl overflow-y-auto p-4 bg-gray-50 rounded-lg shadow-md">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`w-full p-4 rounded-xl mb-2 ${
                  msg.sender === "user"
                    ? "bg-blue-500 text-white self-end"
                    : "bg-gray-200 text-gray-800 self-start"
                }`}
              >
                <ReactMarkdown rehypePlugins={[rehypeRaw]}>
                 {msg.text}
                </ReactMarkdown>
              </div>
            ))}
          </div>
          {/* Área de input y botón */}
          <div className="flex">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Escribe tu mensaje..."
              className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none"
            />
            <button
              onClick={handleSend}
              className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600 transition-colors"
            >
              Enviar
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
}
