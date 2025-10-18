io.write("the i have no ideas quiz :3\n") -- io.write is like print() or std::cout
io.write("this quiz will tell you which random character you are :333\nyou will answer by typing in A, B, C, or D\n")

-- question 1

choices = { -- dictionary for mapping abcd to 1 2 3 4
    ["a"] = 1,
    ["b"] = 2,
    ["c"] = 3,
    ["d"] = 4
}

easy = 0
normal = 0
hard = 0
ext_demon = 0 -- was gonna do GD difficulties, but had no ideas

io.write("1. i am terrible at writing, so just pick one\n")
answer = io.read() -- io.read() takes in a string
answer = string.lower(answer) -- this converts it to lowercase
answer_idx = choices[answer] -- this takes in answer and gets its index

if answer_idx == nil then -- if it's nothing then close the program
    io.write("what\n")
    os.exit()
end

if answer_idx == 1 then -- if answer is a, increment easy
    easy = easy + 1
elseif answer_idx == 2 then
    normal = normal + 1
elseif answer_idx == 3 then
    hard = hard + 1
else
    ext_demon = ext_demon + 1
end -- so on and so forth (why doesn't lua have +=???)