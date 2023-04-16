package gradu.gradu.controller;

import gradu.gradu.dto.BoardDTO;
import gradu.gradu.dto.BoardFileDTO;
import gradu.gradu.service.BoardService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import java.io.IOException;
import java.util.List;

@Controller
@RequiredArgsConstructor
public class BoardController {

    private final BoardService boardService;

    @GetMapping("/write")
    public String saveForm(){
        return "/write";
    }

    @PostMapping("/write")
    public String save(BoardFileDTO boardFileDTO, BoardDTO boardDTO, Model model) throws IOException {
        boardService.save(boardFileDTO, boardDTO);
        model.addAttribute("message","등록이 완료되었습니다");
        model.addAttribute("searchUrl", "/bbs");
        return "message";
    }



    @GetMapping("/bbs")
    public String listForm(Model model) {
        List<BoardDTO> boardDTOS = boardService.findAll();
        model.addAttribute("boardList", boardDTOS);
        return "bbs";
    }


//    @GetMapping("/paging")
//    public String paging(@PageableDefault(page = 1) Pageable pageable, Model model) {
//        //pageable.getPageNumber();
//        Page<BoardDTO> boardList = boardService.paging(pageable);
//        int blockLimit=3;
//        int startPage = (((int)(Math.ceil((double)pageable.getPageNumber() / blockLimit))) - 1) * blockLimit + 1; // 1 4 7 10 ~~
//        int endPage = ((startPage + blockLimit - 1) < boardList.getTotalPages()) ? startPage + blockLimit - 1 : boardList.getTotalPages();
//
//        model.addAttribute("boardList", boardList);
//        model.addAttribute("startPage", startPage);
//        model.addAttribute("endPage", endPage);
//        return "bbs";
//    }
}
