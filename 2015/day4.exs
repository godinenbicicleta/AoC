defmodule Crypto do
  def run(key, num) do
    encoded = :crypto.hash(:md5, "#{key}#{num}") |> Base.encode16()

    case encoded do
      res = "00000" <> _rest -> IO.inspect({res, num})
      _ -> run(key, num + 1)
    end
  end

  def run2(key, num) do
    encoded = :crypto.hash(:md5, "#{key}#{num}") |> Base.encode16()

    case encoded do
      res = "000000" <> _rest -> IO.inspect({res, num})
      _ -> run2(key, num + 1)
    end
  end
end

Crypto.run("ckczppom", 0)
Crypto.run2("ckczppom", 0)
