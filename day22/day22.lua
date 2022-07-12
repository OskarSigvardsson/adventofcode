local function intersection(c1, c2)
    local function i1(l1, l2)
        local min, max = math.min(l1[2], l2[2]), math.max(l1[1], l2[1])
        return max <= min and { max, min }
    end
    local x, y, z = i1(c1[1], c2[1]), i1(c1[2], c2[2]), i1(c1[3], c2[3])
    return x and y and z and { x, y, z } or nil
end
--local clip = 50
local count = 0
local too = { {}, {} }
for line in io.lines(...) do
    local too2 = { {}, {} }
    local o, x1, x2, y1, y2, z1, z2 = line:match("(%a+) x=(%-?%d+)%.%.(%-?%d+),y=(%-?%d+)%.%.(%-?%d+),z=(%-?%d+)%.%.(%-?%d+)")
    local c = { { tonumber(x1), tonumber(x2) }, { tonumber(y1), tonumber(y2) }, { tonumber(z1), tonumber(z2) } }
    if o == "on" then
        table.insert(too2[1], c)
        count = count + (c[1][2] - c[1][1] + 1) * (c[2][2] - c[2][1] + 1) * (c[3][2] - c[3][1] + 1)
    end
    for i, t in ipairs(too) do
        for _, coo in ipairs(t) do
            local ccoo = intersection(c, coo)
            if not ccoo
				or ccoo[1][1] ~= coo[1][1]
				or ccoo[1][2] ~= coo[1][2]
				or ccoo[2][1] ~= coo[2][1]
				or ccoo[2][2] ~= coo[2][2]
				or ccoo[3][1] ~= coo[3][1]
				or ccoo[3][2] ~= coo[3][2] then
                table.insert(too2[3 - i], ccoo)
                table.insert(too2[i], coo)
            end
            if ccoo then
                count = count + (i * 2 - 3) * (ccoo[1][2] - ccoo[1][1] + 1) * (ccoo[2][2] - ccoo[2][1] + 1) * (ccoo[3][2] - ccoo[3][1] + 1)
                -- print(o, ccoo[1][1], ccoo[1][2], ccoo[2][1], ccoo[2][2], ccoo[3][1], ccoo[3][2])
            end
        end
    end
    too = too2
--  io.read()
end
print(count, #too[1], #too[2])
-- count = 0
-- for _, con in ipairs(too[1]) do
--  count = count + (con[1][2] - con[1][1] + 1) * (con[2][2] - con[2][1] + 1) * (con[3][2] - con[3][1] + 1)
-- end
-- for _, coff in ipairs(too[2]) do
--  count = count - (coff[1][2] - coff[1][1] + 1) * (coff[2][2] - coff[2][1] + 1) * (coff[3][2] - coff[3][1] + 1)
-- end
-- print(count)
