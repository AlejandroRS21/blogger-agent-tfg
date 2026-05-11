import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Nuevo Post | BloggerIA",
  description: "Configura y genera un nuevo post editorial utilizando el sistema multi-agente de IA.",
};

export default function NewPostLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
