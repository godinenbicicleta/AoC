defmodule Day24 do
  def main do
    p1() |> IO.inspect()
    p2()
  end

  def p2 do
    particles =
      read()

    pix = particles |> Enum.with_index()

    maxv = +10_000_000_000_000_000_000
    minv = -10_000_000_000_000_000_000

    intersect? = fn [[x, y, z], [dx, dy, dz]] ->
      condition(dx, dy, dz, x, y, z, particles, minv, maxv)
    end

    try do
      for t1 <- 740_740_740_740..1_600_000_000_000,
          delta <- 1..100_000,
          {particle1, ix1} <- pix,
          {particle2, ix2} <- Enum.take(pix, 5),
          ix1 != ix2,
          reduce: [] do
        acc ->
          p1 = [x1, y1, z1] = position_at(particle1, t1)
          p2 = position_at(particle2, t1 + delta)
          [vx, vy, vz] = getv(p2, p1, delta)
          particle0 = [[x1 - vx, y1 - vy, z1 - vz], [vx, vy, vz]]

          conds =
            abs(vx - round(vx)) < 0.0001 and abs(vy - round(vy)) < 0.0001 and
              abs(vz - round(vz)) < 0.0001

          if conds and intersect?.(particle0) do
            throw(particle0)
          else
            acc
          end
      end
    catch
      x -> x
    else
      _ -> nil
    end
  end

  def condition(dx, dy, dz, x, y, z, particles, minv, maxv) do
    Enum.all?(particles, fn p ->
      [[px, py, pz], [vx, vy, vz]] = p

      intersect(p, [[x, y, z], [dx, dy, dz]], minv, maxv, :second) and
        intersect(
          [[pz, px, py], [vz, vx, vy]],
          [[z, x, y], [dz, dx, dy]],
          minv,
          maxv,
          :second
        )
    end)
  end

  def p1 do
    particles =
      read()
      |> Enum.with_index()

    {a, b} = {200_000_000_000_000, 400_000_000_000_000}

    for {p, i} <- particles,
        {q, j} <- particles,
        j > i,
        intersect(p, q, a, b, :first),
        reduce: 0 do
      acc -> acc + 1
    end
  end

  def intersect(
        [[px, py, _pz], [pi, pj, _pk]],
        [[qx, qy, _qz], [qi, qj, _qk]],
        min,
        max,
        part \\ :first
      ) do
    if px == px + pi or qx == qx + qi do
      qx == px or qx + qi == px
    else
      m1 = getm(px, px + pi, py, py + pj)
      m2 = getm(qx, qx + qi, qy, qy + qj)
      b1 = getb(px, px + pi, py, py + pj)
      b2 = getb(qx, qx + qi, qy, qy + qj)

      if m1 - m2 == 0 do
        false
      else
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1

        c1 = if x >= px, do: pi >= 0, else: pi < 0
        c2 = if y >= py, do: pj >= 0, else: pj < 0
        c3 = if x >= qx, do: qi >= 0, else: qi < 0
        c4 = if y >= qy, do: qj >= 0, else: qj < 0
        c5 = x >= min and x <= max
        c6 = y >= min and y <= max
        c7 = abs(x - round(x)) < 0.0001
        c8 = abs(y - round(y)) < 0.0001

        # and
        conds = c1 and c2 and c3 and c4 and c5 and c6

        if part == :first do
          if conds do
            IO.inspect({x, y})
          end

          conds
        else
          conds and c7 and c8
        end

        # intersect([[px, pz, py], [pi, pj, pk]], [[qx, qz, qy], [qi, qk, qj]], min, max)
      end
    end
  end

  def getm(x1, x2, y1, y2) do
    (y2 - y1) / (x2 - x1)
  end

  def getb(x1, x2, y1, y2) do
    y1 - (y2 - y1) * x1 / (x2 - x1)
  end

  def position_at([[px, py, pz], [vx, vy, vz]], t) do
    [px + vx * t, py + vy * t, pz + t * vz]
  end

  def getv([px, py, pz], [x, y, z], t) do
    [(px - x) / t, (py - y) / t, (pz - z) / t]
  end

  def read(fname \\ "") do
    File.stream!("data/day24#{fname}.txt")
    |> Enum.map(fn line ->
      [p, v] =
        line
        |> String.trim()
        |> String.split(" @ ")

      p =
        p
        |> String.split(", ")
        |> Enum.map(fn s ->
          s
          |> String.trim()
          |> String.to_integer()
        end)

      v =
        v
        |> String.split(", ")
        |> Enum.map(fn s ->
          s
          |> String.trim()
          |> String.to_integer()
        end)

      [p, v]
    end)
  end
end
